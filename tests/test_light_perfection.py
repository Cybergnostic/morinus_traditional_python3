"""A3 universal light transfer and exact ephemeris event chronology."""
import unittest
from types import SimpleNamespace
from aspect_event_search import scan, Event
from light_perfection import individual_motion, connections, horary_timeline


def fixture(lons, speeds, contacts):
    p = [SimpleNamespace(data=(l, 0, 0, s)) for l, s in zip(lons, speeds)]
    matrix = [[SimpleNamespace(typ=-1) for _ in range(9)] for _ in range(9)]
    for a, b, k in contacts:
        matrix[max(a, b)][min(a, b)].typ = k
    return SimpleNamespace(planets=SimpleNamespace(planets=p), aspmatrix=matrix)


class LightTests(unittest.TestCase):
    def test_individual_motion(self):
        self.assertEqual(individual_motion(0, 3, 1, 0), 'Applying')
        self.assertEqual(individual_motion(0, 3, -1, 0), 'Separating')
        self.assertEqual(individual_motion(359, 1, 1, 0), 'Applying')

    def test_translation_from_one_to_another(self):
        # Moon separates from Mars and applies to Venus.
        ch = fixture([100, 140, 8, 200, 15, 270, 10],
                     [0, 0, .3, 1, .2, 1, 13],
                     [(6, 2, 0), (6, 4, 0)])
        rows = connections(ch)
        self.assertTrue(any(r.kind == 'Translation' and
            r.actor == 'Moon' and r.source == 'Mars' and
            r.target == 'Venus' for r in rows))

    def test_collection(self):
        # Saturn receives Venus from 10 and Moon from 9.
        ch = fixture([12, 100, 160, 200, 10, 290, 9],
                     [.1, 0, 0, 1, 1, 0, 13],
                     [(0, 4, 0), (0, 6, 0)])
        rows = connections(ch)
        self.assertTrue(any(r.kind == 'Collection' and
            r.actor == 'Saturn' and
            {r.source, r.target} == {'Venus', 'Moon'} for r in rows))

    def test_no_collection_if_feeder_separates(self):
        ch = fixture([12, 100, 160, 200, 14, 290, 9],
                     [.1, 0, 0, 1, 1, 0, 13],
                     [(0, 4, 0), (0, 6, 0)])
        self.assertFalse(any(r.kind == 'Collection' and
                             r.actor == 'Saturn' for r in connections(ch)))

    def test_intervening_station(self):
        events = [Event(1, 'station', 'Moon'),
                  Event(2, 'aspect', 'Venus', 'Moon', 0)]
        ch = fixture([100, 140, 8, 200, 15, 270, 10],
                     [0, 0, .3, 1, .2, 1, 13],
                     [(6, 2, 0), (6, 4, 0)])
        self.assertTrue(any(r.status == 'Interrupted' for
                            r in connections(ch, events)))

    def test_horary_timeline_requires_event_order(self):
        events = [Event(1, 'aspect', 'Moon', 'Venus', 1),
                  Event(2, 'aspect', 'Mars', 'Venus', 2)]
        status, timeline = horary_timeline(events, 'Moon', 'Mars', 30)
        self.assertIn('No exact', status)
        events.append(Event(3, 'aspect', 'Moon', 'Mars', 1))
        status, _ = horary_timeline(events, 'Moon', 'Mars', 30)
        self.assertIn('review impediments', status)


class EphemerisEventTests(unittest.TestCase):
    def linear(self, lons, speeds):
        return lambda t: [((lon + speed * t) % 360, speed)
                          for lon, speed in zip(lons, speeds)]

    def test_exact_contact_and_ingress(self):
        p = self.linear([200, 220, 10, 130, 12, 300, 359],
                        [0, 0, 2, 1, 0, 0, 2])
        es = scan(p, 0, 2, step=.25)
        self.assertTrue(any(e.kind == 'aspect' and
                            {e.first, e.second} == {'Mars', 'Venus'} and
                            abs(e.jd - 1) < 1e-4 for e in es))
        self.assertTrue(any(e.kind == 'ingress' and e.first == 'Moon' and
                            abs(e.jd - .5) < 1e-4 for e in es))

    def test_station_exactly_on_sampling_boundary(self):
        def p(t):
            positions = [(20, 0)] * 7
            positions[5] = (100 + (t - 1) ** 2, 2 * (t - 1))
            return positions
        es = scan(p, 0, 2)
        self.assertTrue(any(e.kind == 'station' and e.first == 'Mercury' and
                            abs(e.jd - 1) < .01 for e in es))

    def test_reverse_ingress_crossing_aries(self):
        p = self.linear([10, 70, 150, 200, 270, 330, 1],
                        [0, 0, 0, 0, 0, 0, -2])
        es = scan(p, 0, 1)
        self.assertTrue(any(e.kind == 'ingress' and e.first == 'Moon' and
                            abs(e.jd - .5) < 1e-4 for e in es))

    def test_invalid_horizon(self):
        with self.assertRaises(ValueError):
            scan(self.linear([0] * 7, [0] * 7), 0, 400)


if __name__ == '__main__':
    unittest.main()
