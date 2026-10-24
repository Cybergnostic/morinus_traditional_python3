"""Dignity-aware reception analysis and native aspect-table data tests."""
import unittest
from types import SimpleNamespace

import aspect_workspace as w


class DummyChart:
    def __init__(self, longs, speeds=None, pairs=(), day=True):
        speeds = speeds or [0.0] * 7
        ps = []
        for i, (lon, speed) in enumerate(zip(longs, speeds)):
            ps.append(SimpleNamespace(data=[lon, 0, 0, speed],
                    speculums=[SimpleNamespace(abovehorizon=day)]))
        self.planets = SimpleNamespace(planets=ps)
        self.aspmatrix = [[SimpleNamespace(typ=-1) for j in range(9)]
                          for i in range(9)]
        for i, j, aspect in pairs:
            self.aspmatrix[max(i,j)][min(i,j)].typ = aspect
        dign = [[[False] * 12 for d in range(2)] for p in range(7)]
        # Mars rules Aries/Scorpio, Venus rules Taurus/Libra.
        for s in (0, 7):
            dign[2][0][s] = True
        for s in (1, 6):
            dign[4][0][s] = True
        # Jupiter exalted in Cancer.
        dign[1][1][3] = True
        trips = [[[-1,-1,-1] for s in range(4)]]
        terms = [[[[0, 30] for k in range(1)] for s in range(12)]]
        decans = [[[-1,-1,-1] for s in range(12)]]
        self.options = SimpleNamespace(dignities=dign, trips=trips, seltrip=0,
            terms=terms, selterm=0, decans=decans, seldecan=0, oneruler=True,
            useexaltationmercury=False, usedaynightorb=False, ayanamsha=0)
        self.ayanamsha = 0
        self.abovehorizonwithorb = day


class WorkspaceTests(unittest.TestCase):
    def test_motion_and_exact(self):
        self.assertEqual(w.angular_motion(0, 63, 2, 0, 60), "Applying")
        self.assertEqual(w.angular_motion(0, 63, 0, 2, 60), "Separating")
        self.assertEqual(w.angular_motion(0, 60, 0, 0, 60), "Exact")
        self.assertEqual(w.angular_motion(0, 63, 0, 0, 60), "Stationary")

    def test_domicile_reception_requires_contact(self):
        # Venus in Mars's Aries; Mars itself makes a degree conjunction.
        ch = DummyChart([180, 130, 10, 65, 11, 230, 350],
                        pairs=[(2,4,0)])
        _, receptions = w.analyze(ch)
        self.assertTrue(any(r.host=="Mars" and r.guest=="Venus"
                            and r.status=="Reception" for r in receptions))

    def test_generosity_without_contact(self):
        ch = DummyChart([180, 130, 10, 65, 12, 230, 350])
        _, receptions = w.analyze(ch)
        self.assertTrue(any(r.host=="Mars" and r.guest=="Venus"
                            and r.status=="Generosity" for r in receptions))

    def test_mutual_reception(self):
        # Mars in Libra, Venus in Aries, in opposition.
        ch = DummyChart([80, 130, 192, 260, 12, 290, 340],
                        pairs=[(2,4,4)])
        _, receptions = w.analyze(ch)
        mutual = [r for r in receptions if r.mutual and r.status == "Reception"]
        self.assertEqual({(r.host, r.guest) for r in mutual},
                         {("Mars","Venus"),("Venus","Mars")})

    def test_one_minor_dignity_does_not_qualify(self):
        ch = DummyChart([80, 130, 192, 260, 40, 290, 340],
                        pairs=[(2,4,1)])
        ch.options.terms[0][1] = [[2,30]]
        self.assertEqual(w.dignity_holds(ch.options, 2, 40, True), ("term",))
        self.assertFalse(w.qualifies_for_reception(("term",)))

    def test_qualifying_minor_pairs(self):
        for x in (("triplicity","term"), ("term","face"),
                  ("triplicity","face")):
            self.assertTrue(w.qualifies_for_reception(x))

    def test_triplicity_changes_with_sect(self):
        ch = DummyChart([80, 130, 192, 260, 40, 290, 340])
        ch.options.trips[0][3] = [2, 1, -1]  # Earth
        self.assertIn("triplicity", w.dignity_holds(ch.options, 2, 40, True))
        self.assertNotIn("triplicity", w.dignity_holds(ch.options, 2, 40, False))

    def test_selected_terms_and_faces(self):
        ch = DummyChart([80, 130, 192, 260, 40, 290, 340])
        ch.options.terms[0][1] = [[2,5],[4,25]]
        ch.options.decans[0][1] = [2,4,0]
        self.assertEqual(w.dignity_holds(ch.options, 2, 32, True), ("term","face"))
        venus_held = w.dignity_holds(ch.options, 4, 42, True)
        self.assertIn("domicile", venus_held)
        self.assertIn("term", venus_held)
        self.assertIn("face", venus_held)

    def test_mercury_virgo_exaltation_setting(self):
        ch = DummyChart([80, 130, 192, 260, 40, 290, 340])
        ch.options.dignities[5][1][5] = True
        self.assertNotIn("exaltation", w.dignity_holds(ch.options, 5, 170, True))
        ch.options.useexaltationmercury = True
        self.assertIn("exaltation", w.dignity_holds(ch.options, 5, 170, True))

    def test_sidereal_position_for_reception(self):
        ch = DummyChart([80, 130, 192, 260, 31, 290, 340])
        ch.options.ayanamsha = 1
        ch.ayanamsha = 23.0
        _, recs = w.analyze(ch)
        self.assertTrue(any(r.host=="Mars" and r.guest=="Venus"
                            and r.guest_sign=="Aries" for r in recs))

    def test_contact_status_and_sort(self):
        ch = DummyChart([80, 130, 192, 260, 12, 290, 340],
                        pairs=[(2,4,4),(0,1,1)],
                        speeds=[0.1,0.0,0.5,1,1,1,1])
        rows,_=w.analyze(ch)
        self.assertEqual(len(rows),2)
        self.assertEqual({r.kind for r in rows},{"Opposition","Sextile"})


if __name__ == "__main__":
    unittest.main()
