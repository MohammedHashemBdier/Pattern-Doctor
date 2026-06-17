"""
PATTERN DOCTOR - DESIGN PATTERN PICKER —  Pattern Knowledge Base (Meta-Reasoning data)
=====================================================================
Knowledge Base Systems Course  —  Damascus University
Faculty of Information Engineering  —  Prof. George Anwar Karaz

This module holds the *declarative knowledge* about each design pattern:
  - category (creational / structural / behavioral)
  - bilingual short description
  - bilingual "Why?" justification  (Lecture 4 — Meta-Reasoning)
  - the reasoning trace (list of rule names / condition strings) that
    justifies the recommendation

It is PURE DATA — no logic, no control flow, no functions.
The rule engine (knowledge_base.py) reads this when it fires a
recommendation rule and asserts an ``Explanation`` fact.
=====================================================================
"""

PATTERNS = {

    # ===================== CREATIONAL =====================
    'Singleton': {
        'category': 'creational',
        'name_ar': 'Singleton (المُفرد)',
        'name_en': 'Singleton',
        'desc_ar': 'يضمن وجود نسخة واحدة فقط من الكائن مع نقطة وصول عامة موحدة.',
        'desc_en': 'Ensures a class has only one instance and provides a global access point.',
        'why_ar': (
            'بما أنك أشرت إلى أن المشكلة تتعلق بإنشاء الكائنات، وتحتاج إلى نسخة '
            'واحدة فقط دون الحاجة لعائلة كائنات، فإن نمط Singleton هو الأنسب '
            'لأنه يضمن نقطة وصول واحدة ويمنع تكرار الكائنات.'
        ),
        'why_en': (
            'Since your problem concerns object creation and you need a single '
            'instance without a family of objects, Singleton is the best fit: '
            'it guarantees one access point and prevents duplicate objects.'
        ),
        'trace': [
            'Q1 = yes  →  category = creational',
            'Q3 = yes  →  needs_single_instance = True',
            'Q5 = no   →  needs_family_of_objects = False',
            'RULE r_rec_singleton FIRED  →  Singleton',
        ],
    },

    'Factory Method': {
        'category': 'creational',
        'name_ar': 'Factory Method (طريقة المصنع)',
        'name_en': 'Factory Method',
        'desc_ar': 'يؤجل تحديد نوع الكائن إلى وقت التشغيل عبر واجهة موحدة للإنشاء.',
        'desc_en': 'Defers the decision of which object to create to runtime via a common interface.',
        'why_ar': (
            'بما أن المشكلة في إنشاء الكائنات، ولا تحتاج نسخة واحدة، لكنك تحتاج '
            'لتأجيل تحديد نوع الكائن إلى وقت التشغيل، فإن Factory Method هو الأنسب '
            'لأنه يفصل الإنشاء عن الاستخدام عبر واجهة موحدة.'
        ),
        'why_en': (
            'Since the problem is about object creation, you do not need a single '
            'instance, but you need to defer the concrete type to runtime, '
            'Factory Method is the best fit: it decouples creation from usage.'
        ),
        'trace': [
            'Q1 = yes  →  category = creational',
            'Q3 = no   →  needs_single_instance = False',
            'Q4 = yes  →  needs_deferred_creation = True',
            'RULE r_rec_factory_method FIRED  →  Factory Method',
        ],
    },

    'Abstract Factory': {
        'category': 'creational',
        'name_ar': 'Abstract Factory (المصنع المجرد)',
        'name_en': 'Abstract Factory',
        'desc_ar': 'يوفر واجهة لإنشاء عائلات من الكائنات المترابطة دون تحديد أصنافها الملموسة.',
        'desc_en': 'Provides an interface for creating families of related objects without specifying concrete classes.',
        'why_ar': (
            'بما أن المشكلة في إنشاء الكائنات وتحتاج لإنشاء عائلة من الكائنات '
            'المترابطة، فإن Abstract Factory هو الأنسب لأنه يضمن توافق الكائنات '
            'داخل العائلة الواحدة عبر واجهة موحدة.'
        ),
        'why_en': (
            'Since the problem is about object creation and you need a family of '
            'related objects, Abstract Factory is the best fit: it ensures the '
            'objects within a family are compatible through a unified interface.'
        ),
        'trace': [
            'Q1 = yes  →  category = creational',
            'Q5 = yes  →  needs_family_of_objects = True',
            'RULE r_rec_abstract_factory FIRED  →  Abstract Factory',
        ],
    },

    # ===================== STRUCTURAL =====================
    'Adapter': {
        'category': 'structural',
        'name_ar': 'Adapter (المُكيِّف)',
        'name_en': 'Adapter',
        'desc_ar': 'يجعل واجهة غير متوافقة تعمل مع واجهة أخرى متوقعة من العميل.',
        'desc_en': 'Makes an incompatible interface work with an interface expected by the client.',
        'why_ar': (
            'بما أن المشكلة في هيكلة الكائنات وتحتاج لجعل واجهة غير متوافقة '
            'تعمل مع واجهة متوقعة، فإن Adapter هو الأنسب لأنه يحوّل واجهة '
            'صنف موجود إلى واجهة أخرى يتوقعها العميل.'
        ),
        'why_en': (
            'Since the problem is about object structure and you need to make an '
            'incompatible interface work with an expected one, Adapter is the best '
            'fit: it converts one interface into another the client expects.'
        ),
        'trace': [
            'Q1 = no, Q2 = yes  →  category = structural',
            'Q6 = yes  →  needs_interface_compat = True',
            'RULE r_rec_adapter FIRED  →  Adapter',
        ],
    },

    'Decorator': {
        'category': 'structural',
        'name_ar': 'Decorator (المُزخرف)',
        'name_en': 'Decorator',
        'desc_ar': 'يضيف سلوكاً لكائن بشكل ديناميكي دون تعديل أصله.',
        'desc_en': 'Adds behavior to an object dynamically without modifying its original class.',
        'why_ar': (
            'بما أن المشكلة هيكلية ولا تحتاج توافق واجهات، لكنك تحتاج لإضافة '
            'سلوك ديناميكياً دون تعديل الأصل، فإن Decorator هو الأنسب لأنه '
            'يلف الكائن بكائنات تضيف سلوكاً جديداً مرناً.'
        ),
        'why_en': (
            'Since the problem is structural, you do not need interface compatibility, '
            'but you need to add behavior dynamically without modifying the original, '
            'Decorator is the best fit: it wraps objects to add behavior flexibly.'
        ),
        'trace': [
            'Q1 = no, Q2 = yes  →  category = structural',
            'Q6 = no, Q7 = yes  →  needs_dynamic_decoration = True',
            'RULE r_rec_decorator FIRED  →  Decorator',
        ],
    },

    'Facade': {
        'category': 'structural',
        'name_ar': 'Facade (الواجهة المبسطة)',
        'name_en': 'Facade',
        'desc_ar': 'يقدم واجهة موحدة مبسطة لنظام فرعي معقد.',
        'desc_en': 'Provides a simplified unified interface to a complex subsystem.',
        'why_ar': (
            'بما أن المشكلة هيكلية ولا تحتاج توافق واجهات أو إضافة سلوك ديناميكي، '
            'لكنك تريد تبسيط نظام فرعي معقد، فإن Facade هو الأنسب لأنه يقدم '
            'واجهة واحدة مبسطة تخفي التعقيد الداخلي.'
        ),
        'why_en': (
            'Since the problem is structural, you do not need interface compatibility '
            'or dynamic decoration, but you want to simplify a complex subsystem, '
            'Facade is the best fit: it offers one simplified interface hiding complexity.'
        ),
        'trace': [
            'Q1 = no, Q2 = yes  →  category = structural',
            'Q6 = no, Q7 = no, Q8 = yes  →  needs_subsystem_simplification = True',
            'RULE r_rec_facade FIRED  →  Facade',
        ],
    },

    # ===================== BEHAVIORAL =====================
    'Command': {
        'category': 'behavioral',
        'name_ar': 'Command (الأمر)',
        'name_en': 'Command',
        'desc_ar': 'يغلّف الطلب ككائن مستقل قابل للتخزين والتأجيل والتراجع.',
        'desc_en': 'Encapsulates a request as an independent object (storable, deferrable, undoable).',
        'why_ar': (
            'بما أن المشكلة سلوكية وتحتاج لتغليف الطلب ككائن مستقل، فإن Command '
            'هو الأنسب لأنه يحوّل الطلب إلى كائن يدعم التأجيل، التخزين، والتراجع.'
        ),
        'why_en': (
            'Since the problem is behavioral and you need to encapsulate a request as '
            'an independent object, Command is the best fit: it turns a request into '
            'an object supporting deferral, storage, and undo.'
        ),
        'trace': [
            'Q1 = no, Q2 = no  →  category = behavioral',
            'Q9 = yes  →  needs_request_encapsulation = True',
            'RULE r_rec_command FIRED  →  Command',
        ],
    },

    'State': {
        'category': 'behavioral',
        'name_ar': 'State (الحالة)',
        'name_en': 'State',
        'desc_ar': 'يغيّر سلوك الكائن تبعاً لحالته الداخلية.',
        'desc_en': "Changes an object's behavior depending on its internal state.",
        'why_ar': (
            'بما أن المشكلة سلوكية ولا تحتاج تغليف الطلب، لكن سلوك الكائن يتغير '
            'تبعاً لحالته الداخلية، فإن State هو الأنسب لأنه يفصل كل حالة في '
            'صنف مستقل ويبدّل السلوك بشفافية.'
        ),
        'why_en': (
            'Since the problem is behavioral, you do not need request encapsulation, '
            'but the behavior changes with the internal state, State is the best fit: '
            'it separates each state into a class and switches behavior transparently.'
        ),
        'trace': [
            'Q1 = no, Q2 = no  →  category = behavioral',
            'Q9 = no, Q10 = yes  →  needs_state_based_behavior = True',
            'RULE r_rec_state FIRED  →  State',
        ],
    },

    'Strategy': {
        'category': 'behavioral',
        'name_ar': 'Strategy (الاستراتيجية)',
        'name_en': 'Strategy',
        'desc_ar': 'يبدّل الخوارزمية المستخدمة وقت التشغيل دون تعديل العميل.',
        'desc_en': 'Swaps the algorithm used at runtime without modifying the client.',
        'why_ar': (
            'بما أن المشكلة سلوكية ولا تحتاج تغليف الطلب أو سلوكاً معتمداً على '
            'الحالة، لكن لديك خوارزميات متعددة قابلة للتبديل، فإن Strategy هو '
            'الأنسب لأنه يغلّف كل خوارزمية ويبدّلها بشفافية.'
        ),
        'why_en': (
            'Since the problem is behavioral, you do not need request encapsulation '
            'or state-based behavior, but you have multiple swappable algorithms, '
            'Strategy is the best fit: it encapsulates each algorithm and swaps it.'
        ),
        'trace': [
            'Q1 = no, Q2 = no  →  category = behavioral',
            'Q9 = no, Q10 = no, Q11 = yes  →  needs_algorithm_variants = True',
            'RULE r_rec_strategy FIRED  →  Strategy',
        ],
    },

    'Observer': {
        'category': 'behavioral',
        'name_ar': 'Observer (المراقب)',
        'name_en': 'Observer',
        'desc_ar': 'يُشعر كائنات متعددة تلقائياً عند تغير حالة كائن ما.',
        'desc_en': 'Automatically notifies multiple objects when another object changes state.',
        'why_ar': (
            'بما أن المشكلة سلوكية وتحتاج لإشعار كائنات متعددة تلقائياً عند '
            'التغيير، فإن Observer هو الأنسب لأنه يبني علاقة (نشر-اشتراك) '
            'بين الموضوع والمراقبين بشكل مرن.'
        ),
        'why_en': (
            'Since the problem is behavioral and you need to automatically notify '
            'multiple objects upon change, Observer is the best fit: it builds a '
            'publish-subscribe relationship between subject and observers.'
        ),
        'trace': [
            'Q1 = no, Q2 = no  →  category = behavioral',
            'Q9 = no, Q10 = no, Q11 = no, Q12 = yes  →  needs_change_notification = True',
            'RULE r_rec_observer FIRED  →  Observer',
        ],
    },

    # ===================== FALLBACK =====================
    'NoSuitablePattern': {
        'category': 'none',
        'name_ar': 'لا يوجد نمط مطابق',
        'name_en': 'No Suitable Pattern',
        'desc_ar': 'لم تتطابق إجاباتك مع أي من الأنماط العشرة المدعومة.',
        'desc_en': 'Your answers did not match any of the ten supported patterns.',
        'why_ar': (
            'بناءً على إجاباتك، لم يتنشّط أي شرط خاص بنمط محدد. قد تكون '
            'المشكلة عامة ولا تتطلب نمطاً، أو قد تحتاج لمراجعة المتطلبات.'
        ),
        'why_en': (
            'Based on your answers, no specific pattern condition was triggered. '
            'The problem may be general and not require a pattern, or you may '
            'need to revisit the requirements.'
        ),
        'trace': [
            'No pattern-specific condition matched',
            'RULE r_rec_fallback FIRED  →  NoSuitablePattern',
        ],
    },
}
