"""
PATTERN DOCTOR - DESIGN PATTERN PICKER —  Expert System
=====================================================================
Knowledge Base Systems Course  —  Damascus University
Faculty of Information Engineering  —  Prof. George Anwar Karaz

Step 1: Fact Class Definitions (Working Memory schema)
---------------------------------------------------------------------
This module contains ONLY declarative knowledge-representation:
  - Fact subclasses (the "types" of facts that can live in Working Memory)
  - Field descriptors with types / defaults

It contains NO rules, NO control flow (if/else/for/while),
NO helper functions, NO I/O.  It is the pure schema layer.

Bilingual (Arabic + English) is baked into the schema from day one,
so every question, justification and recommendation can be shown
in either language.
=====================================================================
"""

from experta import Fact, Field


# ============================================================
# LAYER 1  —  CONTROL / DIALOG-MANAGEMENT FACTS
# (Control Facts: they steer the conversation, REPLACING any
#  imperative while/if-else chain over question stages.)
# ============================================================

class SystemState(Fact):
    """
    الحالة العامة للنظام (Control Fact محوري).

    يحدد المرحلة الحالية من الحوار. توجد حقيقة واحدة فعّالة فقط
    في الذاكرة العاملة في كل لحظة. القواعد تعدّل قيمة ``current_stage``
    لتنتقل من سؤال إلى سؤال دون استخدام while / if.

    The single "where are we in the dialog?" fact.
    Exactly one instance is active at any time.
    """
    current_stage = Field(str, mandatory=True)


class PendingQuestion(Fact):
    """
    سؤال ينتظر إجابة المستخدم.

    عندما تُصرَّح هذه الحقيقة، فإن طبقة الإدخال/الإخراج الرفيعة
    (والتي لا تحتوي على أي منطق قرار) تقرأها، تعرض نص السؤال،
    تجمع الجواب، ثم تُصرِّح ``UserAnswer``.

    A question awaiting the user's answer.
    The thin I/O shell reads this fact, shows the question,
    collects the answer, then asserts a UserAnswer fact.
    """
    qid = Field(str, mandatory=True)


class DialogComplete(Fact):
    """
    علم انتهاء الحوار.

    يُصرَّح عندما تصل القواعد إلى توصية نهائية وجاهزة للعرض.

    Marker fact: the dialog is finished and a recommendation
    is ready to be displayed to the user.
    """
    pass


# ============================================================
# LAYER 2  —  USER INPUT FACT
# ============================================================

class UserAnswer(Fact):
    """
    إجابة المستخدم على سؤال معيّن.

    A single answer provided by the user for a given question.
    ``value`` ∈ {'yes', 'no', 'maybe'}.
    """
    question_id = Field(str, mandatory=True)
    value       = Field(str, mandatory=True)


# ============================================================
# LAYER 3  —  QUESTION CATALOG FACT (static, declared at startup)
# ============================================================

class Question(Fact):
    """
    بند سؤال من فهرس الأسئلة (ثابت).

    تُصرَّح كل الأسئلة مرة واحدة عند إقلاع المحرك كحقائق ثابتة.
    النصوص ثنائية اللغة (عربي/إنكليزي) دعماً لمتطلب المشروع.

    A question entry. All Question facts are declared once at
    engine startup. Bilingual text supports the Arabic/English
    requirement of the project.
    """
    qid     = Field(str, mandatory=True)
    text_ar = Field(str, mandatory=True)
    text_en = Field(str, mandatory=True)


# ============================================================
# LAYER 4  —  DERIVED CONTEXT FACT  (intermediate knowledge)
# (Rules MODIFY these boolean flags as answers arrive — this is
#  the "context filtering" layer that precedes pattern matching.
#  Exactly ONE Context fact exists in working memory.)
# ============================================================

class Context(Fact):
    """
    سياق المشكلة المتراكم من إجابات المستخدم.

    Aggregated problem context.  Rules MODIFY these boolean flags
    as the user answers questions.  Exactly one Context fact exists.

    The 10 flags below are sufficient to discriminate among the
    10 target design patterns without overlap:
      Creational  : Singleton, Factory Method, Abstract Factory
      Structural  : Adapter, Decorator, Facade
      Behavioral  : Command, Observer, State, Strategy
    """
    # --- Category (set first by the very first answer) ---
    category = Field(str,  default='unknown')   # creational | structural | behavioral

    # --- Creational signals ---
    needs_single_instance          = Field(bool, default=False)
    needs_deferred_creation        = Field(bool, default=False)
    needs_family_of_objects        = Field(bool, default=False)

    # --- Structural signals ---
    needs_interface_compat         = Field(bool, default=False)
    needs_dynamic_decoration       = Field(bool, default=False)
    needs_subsystem_simplification = Field(bool, default=False)

    # --- Behavioral signals ---
    needs_request_encapsulation    = Field(bool, default=False)
    needs_state_based_behavior     = Field(bool, default=False)
    needs_algorithm_variants       = Field(bool, default=False)
    needs_change_notification      = Field(bool, default=False)


# ============================================================
# LAYER 5  —  OUTPUT FACTS  (recommendation + explanation)
# ============================================================

class RecommendedPattern(Fact):
    """
    النمط المُقترَح (الناتج النهائي).

    The final recommended design pattern.
    """
    pattern_name = Field(str, mandatory=True)
    category     = Field(str, mandatory=True)


class Explanation(Fact):
    """
    تفسير التوصية  —  ميزة "Why؟".

    This is the Meta-Reasoning artifact required by Lecture 4.
    When a recommendation rule fires, it ALSO declares an
    Explanation fact storing:
      - the pattern name it justifies,
      - a bilingual human-readable justification,
      - the ordered list of rule names that contributed to the
        conclusion (the reasoning path).

    The user can later query "Why?" and the system reconstructs
    the argument purely from these Explanation facts — no extra
    inference, no procedural reconstruction code.
    """
    pattern_name     = Field(str,  mandatory=True)
    justification_ar = Field(str,  default='')
    justification_en = Field(str,  default='')
    fired_rules      = Field(list, default=[])


# ============================================================
# End of Step 1.
# The next module (rules_dialog.py, Step 2) will import these
# facts and write the @Rule decorators that drive the dialog.
# ============================================================
