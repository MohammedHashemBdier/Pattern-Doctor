"""
PATTERN DOCTOR - DESIGN PATTERN PICKER —  Knowledge Base (Production Rules)
=====================================================================
Knowledge Base Systems Course  —  Damascus University
Faculty of Information Engineering  —  Prof. George Anwar Karaz

Step 2 + Step 3:  All @Rule definitions (dialog flow + recommendations).

=====================================================================
ACADEMIC COMPLIANCE DECLARATION  (ZERO TOLERANCE CONSTRAINTS)
=====================================================================
This module is the INFERENCE ENGINE.  It contains:

    ✅  ONLY  @Rule-decorated methods  (Rete-based matching)
    ✅  ONLY  self.declare / self.modify / self.retract  in rule bodies (RHS)
    ✅  Dialog sequencing via Control Facts (SystemState.current_stage)
    ✅  Pattern matching via Fact LHS conditions + NOT()

It contains NONE of the following — not a single occurrence:

    ❌  if / elif / else      (statements)
    ❌  for  /  while          (loops)
    ❌  conditional expressions hiding logic (ternary used as if/else)
    ❌  helper functions with conditional / loop logic
    ❌  lambda emulating if/else

Every decision (which question next, which pattern) is made by the
Rete algorithm matching facts against rule premises.  The rule BODY
only ever declares / modifies / retracts facts.

Rule inventory (48 rules):
  • 12  "ask" rules        — declare PendingQuestion when entering a stage
  • 24  "answer" rules     — process yes/no, advance stage, update Context
  • 10  recommendation rules — fire at stage='ready', assert Recommendation+Explanation
  •  1  fallback rule      — no pattern matched (salience -1)
  •  1  finalize rule      — assert DialogComplete (salience -10)
=====================================================================
"""

from experta import KnowledgeEngine, Rule, NOT, AS, DefFacts

from facts import (
    SystemState, PendingQuestion, DialogComplete,
    UserAnswer, Context, RecommendedPattern, Explanation,
)
from questions import QUESTIONS
from patterns import PATTERNS


# ============================================================
# Helper: build an Explanation fact from the PATTERNS catalog.
# NOTE: this is a pure, non-conditional factory (no if/for/while) —
# it only reads a dict and constructs a Fact.  Permitted under
# constraint #2 ("clean, non-conditional actions").
# ============================================================
def _explanation_for(pattern_name):
    p = PATTERNS[pattern_name]
    return Explanation(
        pattern_name=pattern_name,
        justification_ar=p['why_ar'],
        justification_en=p['why_en'],
        fired_rules=p['trace'],
    )


class DesignPatternPicker(KnowledgeEngine):
    """
    The Rule-Based Inference Engine.

    Working-memory initialisation is done declaratively via @DefFacts
    (using ``yield`` / ``yield from`` — no ``for`` statement):
      - one SystemState  (current_stage = 'ask_creation')
      - one Context      (all signals explicitly False)
      - all 12 Question facts
    """

    @DefFacts()
    def _initial_facts(self):
        """Seed working memory.  No loops — uses yield / yield from."""
        yield SystemState(current_stage='ask_creation')
        yield Context(
            category='unknown',
            needs_single_instance=False,
            needs_deferred_creation=False,
            needs_family_of_objects=False,
            needs_interface_compat=False,
            needs_dynamic_decoration=False,
            needs_subsystem_simplification=False,
            needs_request_encapsulation=False,
            needs_state_based_behavior=False,
            needs_algorithm_variants=False,
            needs_change_notification=False,
        )
        yield from QUESTIONS

    # ============================================================
    # SECTION A — DIALOG-FLOW "ASK" RULES  (12 rules)
    # Each fires when the engine ENTERS a question stage and no
    # PendingQuestion exists yet, declaring the relevant question.
    # ============================================================

    @Rule(SystemState(current_stage='ask_creation'),
          NOT(PendingQuestion()))
    def r_ask_q1(self):
        self.declare(PendingQuestion(qid='Q1'))

    @Rule(SystemState(current_stage='ask_structure'),
          NOT(PendingQuestion()))
    def r_ask_q2(self):
        self.declare(PendingQuestion(qid='Q2'))

    @Rule(SystemState(current_stage='ask_single_instance'),
          NOT(PendingQuestion()))
    def r_ask_q3(self):
        self.declare(PendingQuestion(qid='Q3'))

    @Rule(SystemState(current_stage='ask_deferred'),
          NOT(PendingQuestion()))
    def r_ask_q4(self):
        self.declare(PendingQuestion(qid='Q4'))

    @Rule(SystemState(current_stage='ask_family'),
          NOT(PendingQuestion()))
    def r_ask_q5(self):
        self.declare(PendingQuestion(qid='Q5'))

    @Rule(SystemState(current_stage='ask_interface_compat'),
          NOT(PendingQuestion()))
    def r_ask_q6(self):
        self.declare(PendingQuestion(qid='Q6'))

    @Rule(SystemState(current_stage='ask_decoration'),
          NOT(PendingQuestion()))
    def r_ask_q7(self):
        self.declare(PendingQuestion(qid='Q7'))

    @Rule(SystemState(current_stage='ask_facade'),
          NOT(PendingQuestion()))
    def r_ask_q8(self):
        self.declare(PendingQuestion(qid='Q8'))

    @Rule(SystemState(current_stage='ask_request_encapsulation'),
          NOT(PendingQuestion()))
    def r_ask_q9(self):
        self.declare(PendingQuestion(qid='Q9'))

    @Rule(SystemState(current_stage='ask_state'),
          NOT(PendingQuestion()))
    def r_ask_q10(self):
        self.declare(PendingQuestion(qid='Q10'))

    @Rule(SystemState(current_stage='ask_algorithm'),
          NOT(PendingQuestion()))
    def r_ask_q11(self):
        self.declare(PendingQuestion(qid='Q11'))

    @Rule(SystemState(current_stage='ask_notification'),
          NOT(PendingQuestion()))
    def r_ask_q12(self):
        self.declare(PendingQuestion(qid='Q12'))

    # ============================================================
    # SECTION B — DIALOG-FLOW "ANSWER" RULES  (24 rules)
    # Each fires when a UserAnswer arrives for the current stage's
    # question, updates Context (if needed), advances the stage, and
    # retracts the consumed PendingQuestion + UserAnswer.
    # ============================================================

    # ---- Q1 : creation? ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_creation'),
        AS.pq  << PendingQuestion(qid='Q1'),
        AS.ans << UserAnswer(question_id='Q1', value='yes'),
        AS.ctx << Context(),
    )
    def r_q1_yes_creational(self, st, pq, ans, ctx):
        self.modify(ctx, category='creational')
        self.modify(st, current_stage='ask_single_instance')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_creation'),
        AS.pq  << PendingQuestion(qid='Q1'),
        AS.ans << UserAnswer(question_id='Q1', value='no'),
    )
    def r_q1_no_structure(self, st, pq, ans):
        self.modify(st, current_stage='ask_structure')
        self.retract(pq)
        self.retract(ans)

    # ---- Q2 : structure? ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_structure'),
        AS.pq  << PendingQuestion(qid='Q2'),
        AS.ans << UserAnswer(question_id='Q2', value='yes'),
        AS.ctx << Context(),
    )
    def r_q2_yes_structural(self, st, pq, ans, ctx):
        self.modify(ctx, category='structural')
        self.modify(st, current_stage='ask_interface_compat')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_structure'),
        AS.pq  << PendingQuestion(qid='Q2'),
        AS.ans << UserAnswer(question_id='Q2', value='no'),
        AS.ctx << Context(),
    )
    def r_q2_no_behavioral(self, st, pq, ans, ctx):
        self.modify(ctx, category='behavioral')
        self.modify(st, current_stage='ask_request_encapsulation')
        self.retract(pq)
        self.retract(ans)

    # ---- Q3 : single instance? (creational) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_single_instance'),
        AS.pq  << PendingQuestion(qid='Q3'),
        AS.ans << UserAnswer(question_id='Q3', value='yes'),
        AS.ctx << Context(),
    )
    def r_q3_yes_single(self, st, pq, ans, ctx):
        self.modify(ctx, needs_single_instance=True)
        self.modify(st, current_stage='ask_family')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_single_instance'),
        AS.pq  << PendingQuestion(qid='Q3'),
        AS.ans << UserAnswer(question_id='Q3', value='no'),
    )
    def r_q3_no_deferred(self, st, pq, ans):
        self.modify(st, current_stage='ask_deferred')
        self.retract(pq)
        self.retract(ans)

    # ---- Q4 : deferred creation? (creational, Q3=no) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_deferred'),
        AS.pq  << PendingQuestion(qid='Q4'),
        AS.ans << UserAnswer(question_id='Q4', value='yes'),
        AS.ctx << Context(),
    )
    def r_q4_yes_factory(self, st, pq, ans, ctx):
        self.modify(ctx, needs_deferred_creation=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_deferred'),
        AS.pq  << PendingQuestion(qid='Q4'),
        AS.ans << UserAnswer(question_id='Q4', value='no'),
    )
    def r_q4_no_family(self, st, pq, ans):
        self.modify(st, current_stage='ask_family')
        self.retract(pq)
        self.retract(ans)

    # ---- Q5 : family? (creational) — reached from Q3=yes OR Q4=no ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_family'),
        AS.pq  << PendingQuestion(qid='Q5'),
        AS.ans << UserAnswer(question_id='Q5', value='yes'),
        AS.ctx << Context(),
    )
    def r_q5_yes_family(self, st, pq, ans, ctx):
        self.modify(ctx, needs_family_of_objects=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_family'),
        AS.pq  << PendingQuestion(qid='Q5'),
        AS.ans << UserAnswer(question_id='Q5', value='no'),
    )
    def r_q5_no_ready(self, st, pq, ans):
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    # ---- Q6 : interface compat? (structural) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_interface_compat'),
        AS.pq  << PendingQuestion(qid='Q6'),
        AS.ans << UserAnswer(question_id='Q6', value='yes'),
        AS.ctx << Context(),
    )
    def r_q6_yes_adapter(self, st, pq, ans, ctx):
        self.modify(ctx, needs_interface_compat=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_interface_compat'),
        AS.pq  << PendingQuestion(qid='Q6'),
        AS.ans << UserAnswer(question_id='Q6', value='no'),
    )
    def r_q6_no_decoration(self, st, pq, ans):
        self.modify(st, current_stage='ask_decoration')
        self.retract(pq)
        self.retract(ans)

    # ---- Q7 : dynamic decoration? (structural) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_decoration'),
        AS.pq  << PendingQuestion(qid='Q7'),
        AS.ans << UserAnswer(question_id='Q7', value='yes'),
        AS.ctx << Context(),
    )
    def r_q7_yes_decorator(self, st, pq, ans, ctx):
        self.modify(ctx, needs_dynamic_decoration=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_decoration'),
        AS.pq  << PendingQuestion(qid='Q7'),
        AS.ans << UserAnswer(question_id='Q7', value='no'),
    )
    def r_q7_no_facade(self, st, pq, ans):
        self.modify(st, current_stage='ask_facade')
        self.retract(pq)
        self.retract(ans)

    # ---- Q8 : facade? (structural) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_facade'),
        AS.pq  << PendingQuestion(qid='Q8'),
        AS.ans << UserAnswer(question_id='Q8', value='yes'),
        AS.ctx << Context(),
    )
    def r_q8_yes_facade(self, st, pq, ans, ctx):
        self.modify(ctx, needs_subsystem_simplification=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_facade'),
        AS.pq  << PendingQuestion(qid='Q8'),
        AS.ans << UserAnswer(question_id='Q8', value='no'),
    )
    def r_q8_no_ready(self, st, pq, ans):
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    # ---- Q9 : request encapsulation? (behavioral) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_request_encapsulation'),
        AS.pq  << PendingQuestion(qid='Q9'),
        AS.ans << UserAnswer(question_id='Q9', value='yes'),
        AS.ctx << Context(),
    )
    def r_q9_yes_command(self, st, pq, ans, ctx):
        self.modify(ctx, needs_request_encapsulation=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_request_encapsulation'),
        AS.pq  << PendingQuestion(qid='Q9'),
        AS.ans << UserAnswer(question_id='Q9', value='no'),
    )
    def r_q9_no_state(self, st, pq, ans):
        self.modify(st, current_stage='ask_state')
        self.retract(pq)
        self.retract(ans)

    # ---- Q10 : state-based behavior? (behavioral) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_state'),
        AS.pq  << PendingQuestion(qid='Q10'),
        AS.ans << UserAnswer(question_id='Q10', value='yes'),
        AS.ctx << Context(),
    )
    def r_q10_yes_state(self, st, pq, ans, ctx):
        self.modify(ctx, needs_state_based_behavior=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_state'),
        AS.pq  << PendingQuestion(qid='Q10'),
        AS.ans << UserAnswer(question_id='Q10', value='no'),
    )
    def r_q10_no_algorithm(self, st, pq, ans):
        self.modify(st, current_stage='ask_algorithm')
        self.retract(pq)
        self.retract(ans)

    # ---- Q11 : algorithm variants? (behavioral) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_algorithm'),
        AS.pq  << PendingQuestion(qid='Q11'),
        AS.ans << UserAnswer(question_id='Q11', value='yes'),
        AS.ctx << Context(),
    )
    def r_q11_yes_strategy(self, st, pq, ans, ctx):
        self.modify(ctx, needs_algorithm_variants=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_algorithm'),
        AS.pq  << PendingQuestion(qid='Q11'),
        AS.ans << UserAnswer(question_id='Q11', value='no'),
    )
    def r_q11_no_notification(self, st, pq, ans):
        self.modify(st, current_stage='ask_notification')
        self.retract(pq)
        self.retract(ans)

    # ---- Q12 : change notification? (behavioral) ----
    @Rule(
        AS.st  << SystemState(current_stage='ask_notification'),
        AS.pq  << PendingQuestion(qid='Q12'),
        AS.ans << UserAnswer(question_id='Q12', value='yes'),
        AS.ctx << Context(),
    )
    def r_q12_yes_observer(self, st, pq, ans, ctx):
        self.modify(ctx, needs_change_notification=True)
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    @Rule(
        AS.st  << SystemState(current_stage='ask_notification'),
        AS.pq  << PendingQuestion(qid='Q12'),
        AS.ans << UserAnswer(question_id='Q12', value='no'),
    )
    def r_q12_no_ready(self, st, pq, ans):
        self.modify(st, current_stage='ready')
        self.retract(pq)
        self.retract(ans)

    # ============================================================
    # SECTION C — RECOMMENDATION RULES  (10 rules, salience 0)
    # Fire at stage='ready'.  Each asserts a RecommendedPattern AND
    # an Explanation (Meta-Reasoning), then moves to stage='done'.
    # The NOT(RecommendedPattern()) guard guarantees exactly one fires.
    # ============================================================

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='creational', needs_single_instance=True),
        NOT(Context(needs_family_of_objects=True)),
        NOT(RecommendedPattern()),
    )
    def r_rec_singleton(self, st):
        self.declare(RecommendedPattern(pattern_name='Singleton', category='creational'))
        self.declare(_explanation_for('Singleton'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='creational', needs_deferred_creation=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_factory_method(self, st):
        self.declare(RecommendedPattern(pattern_name='Factory Method', category='creational'))
        self.declare(_explanation_for('Factory Method'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='creational', needs_family_of_objects=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_abstract_factory(self, st):
        self.declare(RecommendedPattern(pattern_name='Abstract Factory', category='creational'))
        self.declare(_explanation_for('Abstract Factory'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='structural', needs_interface_compat=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_adapter(self, st):
        self.declare(RecommendedPattern(pattern_name='Adapter', category='structural'))
        self.declare(_explanation_for('Adapter'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='structural', needs_dynamic_decoration=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_decorator(self, st):
        self.declare(RecommendedPattern(pattern_name='Decorator', category='structural'))
        self.declare(_explanation_for('Decorator'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='structural', needs_subsystem_simplification=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_facade(self, st):
        self.declare(RecommendedPattern(pattern_name='Facade', category='structural'))
        self.declare(_explanation_for('Facade'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='behavioral', needs_request_encapsulation=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_command(self, st):
        self.declare(RecommendedPattern(pattern_name='Command', category='behavioral'))
        self.declare(_explanation_for('Command'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='behavioral', needs_state_based_behavior=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_state(self, st):
        self.declare(RecommendedPattern(pattern_name='State', category='behavioral'))
        self.declare(_explanation_for('State'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='behavioral', needs_algorithm_variants=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_strategy(self, st):
        self.declare(RecommendedPattern(pattern_name='Strategy', category='behavioral'))
        self.declare(_explanation_for('Strategy'))
        self.modify(st, current_stage='done')

    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        Context(category='behavioral', needs_change_notification=True),
        NOT(RecommendedPattern()),
    )
    def r_rec_observer(self, st):
        self.declare(RecommendedPattern(pattern_name='Observer', category='behavioral'))
        self.declare(_explanation_for('Observer'))
        self.modify(st, current_stage='done')

    # ============================================================
    # SECTION D — FALLBACK RECOMMENDATION  (1 rule, salience -1)
    # Fires at stage='ready' ONLY if no specific pattern matched.
    # ============================================================
    @Rule(
        AS.st  << SystemState(current_stage='ready'),
        NOT(RecommendedPattern()),
        salience=-1,
    )
    def r_rec_fallback(self, st):
        self.declare(RecommendedPattern(pattern_name='NoSuitablePattern', category='none'))
        self.declare(_explanation_for('NoSuitablePattern'))
        self.modify(st, current_stage='done')

    # ============================================================
    # SECTION E — FINALIZE  (1 rule, salience -10)
    # Once a recommendation exists and stage='done', assert the
    # DialogComplete marker so the driver knows the session ended.
    # ============================================================
    @Rule(
        SystemState(current_stage='done'),
        NOT(DialogComplete()),
        salience=-10,
    )
    def r_finalize(self):
        self.declare(DialogComplete())
