"""Syntax mapping: Zed syntax key -> IntelliJ attribute ids (per language).

Populated by the syntax-attributes ticket (04b). Every IntelliJ id is a verified
``TextAttributesKey`` *name* - never an invented id - taken from one of the
sources below (names only; all color values come from the pinned palette via the
generator):

* Platform defaults - IDEA-bundled ``intellij.platform.core.jar``,
  ``com.intellij.openapi.editor.DefaultLanguageHighlighterColors`` (the
  ``DEFAULT_*`` keys plus the base scheme punctuation keys BRACES / BRACKETS /
  PARENTHS / DOT / SEMICOLON / COMMA / OPERATION_SIGN).
* Java - ``intellij.java.frontback.psi.impl.jar``,
  ``com.intellij.ide.highlighter.JavaHighlightingColors`` (the ``JAVA_*`` keys and
  the ``*_ATTRIBUTES`` family; Java registers e.g.
  ``LOCAL_VARIABLE_ATTRIBUTES`` / ``CLASS_NAME_ATTRIBUTES`` rather than the plain
  platform names).
* JavaScript / TypeScript - WebStorm harvest recorded in ticket 01
  (:data:`JS_ATTRIBUTE_IDS`, :data:`TS_ATTRIBUTE_IDS`).
* Kotlin - IDEA-bundled Kotlin plugin harvest recorded in ticket 01
  (:data:`KOTLIN_ATTRIBUTE_IDS`).
* JSON - IDEA-bundled ``plugins/json/lib/intellij.json.jar``,
  ``com.intellij.json.highlighting.JsonSyntaxHighlighterFactory`` (dotted
  ``JSON.*`` namespace).
* Python - PyCharm OSS source at
  ``intellij-community/python/python-syntax-core/src/com/jetbrains/python/highlighting/PyHighlighter.java``
  and ``.../python-syntax/src/com/jetbrains/python/highlighting/PythonColorsPage.java``
  (dotted ``PY.*`` namespace).

Roles whose Zed color has no confidently-enumerable IntelliJ key are routed to a
semantically nearest verified platform DEFAULT where one exists (for example
``link_text`` -> ``DEFAULT_HIGHLIGHTED_REFERENCE``); the remainder are listed in
:data:`UNRESOLVED_ROLE_FALLBACKS` and inherit the parent scheme default instead of
being guessed.

Duplicate attribute ids across Zed roles are permitted here because the generator
deduplicates by id on emission (first occurrence wins), so an id shared by two
roles produces exactly one ``<option>`` entry carrying the first-listed role's
value. Order shared-id entries from most specific to most general.

Values are driven per variant from the pinned palette; Night, Storm and Moon do
not share every value (see CONTEXT.md), so no literal colors appear here.
"""

from __future__ import annotations

# JavaScript external TextAttributesKey names (WebStorm JavaScriptHighlightDescriptor).
JS_ATTRIBUTE_IDS: tuple[str, ...] = (
    "JS.KEYWORD",
    "JS.STRING",
    "JS.NUMBER",
    "JS.REGEXP",
    "JS.LINE_COMMENT",
    "JS.BLOCK_COMMENT",
    "JS.DOC_COMMENT",
    "JS.OPERATION_SIGN",
    "JS.PARENTHS",
    "JS.BRACKETS",
    "JS.BRACES",
    "JS.COMMA",
    "JS.DOT",
    "JS.SEMICOLON",
    "JS.BADCHARACTER",
    "JS.DOC_TAG",
    "JS.DOC_TAG_NAMEPATH",
    "JS.DOC_TYPE",
    "JS.VALID_STRING_ESCAPE",
    "JS.INVALID_STRING_ESCAPE",
    "JS.LOCAL_VARIABLE",
    "JS.PARAMETER",
    "JS.INSTANCE_MEMBER_VARIABLE",
    "JS.STATIC_MEMBER_VARIABLE",
    "JS.GLOBAL_VARIABLE",
    "JS.GLOBAL_FUNCTION",
    "JS.LOCAL_FUNCTION",
    "JS.DECORATOR",
    "JS.STATIC_MEMBER_FUNCTION",
    "JS.INSTANCE_MEMBER_FUNCTION",
    "JS.CLASS",
    "JS.INTERFACE",
    "JS.TYPE_ALIAS",
    "JS.LABEL",
    "JS.MODULE_NAME",
    "JS.FUNCTION_ARROW",
    "JS.PRIMITIVE.TYPE",
    "JS.EXPORTED.VARIABLE",
    "JS.EXPORTED.FUNCTION",
    "JS.EXPORTED.CLASS",
    "JS.JSX_CLIENT_COMPONENT",
    "JS.TEMPLATE_LITERAL_PLACEHOLDER_DELIMITERS",
)

# TypeScript external TextAttributesKey names (WebStorm TypeScriptHighlighter).
# Dotted suffixes (TS.TYPE.ALIAS, TS.PRIMITIVE.TYPES) are the literal registered
# spellings used upstream, not typos.
TS_ATTRIBUTE_IDS: tuple[str, ...] = (
    "TS.KEYWORD",
    "TS.STRING",
    "TS.NUMBER",
    "TS.REGEXP",
    "TS.LINE_COMMENT",
    "TS.BLOCK_COMMENT",
    "TS.DOC_COMMENT",
    "TS.OPERATION_SIGN",
    "TS.PARENTHS",
    "TS.BRACKETS",
    "TS.BRACES",
    "TS.COMMA",
    "TS.DOT",
    "TS.SEMICOLON",
    "TS.BADCHARACTER",
    "TS.DOC_TAG",
    "TS.DOC_TAG_NAMEPATH",
    "TS.DOC_TYPE",
    "TS.VALID_STRING_ESCAPE",
    "TS.INVALID_STRING_ESCAPE",
    "TS.LOCAL_VARIABLE",
    "TS.PARAMETER",
    "TS.INSTANCE_MEMBER_VARIABLE",
    "TS.STATIC_MEMBER_VARIABLE",
    "TS.GLOBAL_VARIABLE",
    "TS.GLOBAL_FUNCTION",
    "TS.LOCAL_FUNCTION",
    "TS.DECORATOR",
    "TS.STATIC_MEMBER_FUNCTION",
    "TS.INSTANCE_MEMBER_FUNCTION",
    "TS.CLASS",
    "TS.INTERFACE",
    "TS.TYPE_GUARD",
    "TS.TYPE.ALIAS",
    "TS.PRIMITIVE.TYPES",
    "TS.FUNCTION_ARROW",
    "TS.EXPORTED_VARIABLE",
    "TS.EXPORTED_FUNCTION",
    "TS.EXPORTED_CLASS",
    "TS.LABEL",
    "TS.TEMPLATE_LITERAL_PLACEHOLDER_DELIMITERS",
)

# Kotlin external TextAttributesKey names (KotlinHighlightingColors).
KOTLIN_ATTRIBUTE_IDS: tuple[str, ...] = (
    "KDOC_LINK",
    "KDOC_TAG_NAME",
    "KOTLIN_ABSTRACT_CLASS",
    "KOTLIN_AMPERSAND",
    "KOTLIN_ANDROID_EXTENSIONS_PROPERTY_CALL",
    "KOTLIN_ANNOTATION",
    "KOTLIN_ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES",
    "KOTLIN_ARROW",
    "KOTLIN_BACKING_FIELD_VARIABLE",
    "KOTLIN_BAD_CHARACTER",
    "KOTLIN_BLOCK_COMMENT",
    "KOTLIN_BRACES",
    "KOTLIN_BRACKETS",
    "KOTLIN_BUILTIN_ANNOTATION",
    "KOTLIN_CLASS",
    "KOTLIN_CLOSURE_DEFAULT_PARAMETER",
    "KOTLIN_COLON",
    "KOTLIN_COMMA",
    "KOTLIN_CONSTRUCTOR",
    "KOTLIN_CONTEXT_ARGUMENT",
    "KOTLIN_DATA_CLASS",
    "KOTLIN_DATA_OBJECT",
    "KOTLIN_DEBUG_INFO",
    "KOTLIN_DOC_COMMENT",
    "KOTLIN_DOT",
    "KOTLIN_DOUBLE_COLON",
    "KOTLIN_DYNAMIC_FUNCTION_CALL",
    "KOTLIN_DYNAMIC_PROPERTY_CALL",
    "KOTLIN_ENUM",
    "KOTLIN_ENUM_ENTRY",
    "KOTLIN_EXCLEXCL",
    "KOTLIN_EXTENSION_FUNCTION_CALL",
    "KOTLIN_EXTENSION_PROPERTY",
    "KOTLIN_FUNCTION_CALL",
    "KOTLIN_FUNCTION_DECLARATION",
    "KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW",
    "KOTLIN_INSTANCE_PROPERTY",
    "KOTLIN_INSTANCE_PROPERTY_CUSTOM_PROPERTY_DECLARATION",
    "KOTLIN_INVALID_STRING_ESCAPE",
    "KOTLIN_KEYWORD",
    "KOTLIN_KEYWORD_VAL",
    "KOTLIN_KEYWORD_VAR",
    "KOTLIN_LABEL",
    "KOTLIN_LINE_COMMENT",
    "KOTLIN_LOCAL_VARIABLE",
    "KOTLIN_MUTABLE_VARIABLE",
    "KOTLIN_NAMED_ARGUMENT",
    "KOTLIN_NUMBER",
    "KOTLIN_OBJECT",
    "KOTLIN_OPERATION_SIGN",
    "KOTLIN_PACKAGE_FUNCTION_CALL",
    "KOTLIN_PACKAGE_PROPERTY",
    "KOTLIN_PACKAGE_PROPERTY_CUSTOM_PROPERTY_DECLARATION",
    "KOTLIN_PARAMETER",
    "KOTLIN_PARENTHESIS",
    "KOTLIN_QUEST",
    "KOTLIN_RESOLVED_TO_ERROR",
    "KOTLIN_SAFE_ACCESS",
    "KOTLIN_SEMICOLON",
    "KOTLIN_SMART_CAST_RECEIVER",
    "KOTLIN_SMART_CAST_VALUE",
    "KOTLIN_SMART_CONSTANT",
    "KOTLIN_STRING",
    "KOTLIN_STRING_ESCAPE",
    "KOTLIN_SUSPEND_FUNCTION_CALL",
    "KOTLIN_SYNTHETIC_EXTENSION_PROPERTY",
    "KOTLIN_TRAIT",
    "KOTLIN_TYPE_ALIAS",
    "KOTLIN_TYPE_PARAMETER",
    "KOTLIN_VARIABLE_AS_FUNCTION",
    "KOTLIN_VARIABLE_AS_FUNCTION_LIKE",
    "KOTLIN_WRAPPED_INTO_REF",
)

# Platform default TextAttributesKey names (DefaultLanguageHighlighterColors).
PLATFORM_ATTRIBUTE_IDS: tuple[str, ...] = (
    "DEFAULT_ATTRIBUTE",
    "DEFAULT_BLOCK_COMMENT",
    "DEFAULT_BRACES",
    "DEFAULT_BRACKETS",
    "DEFAULT_CLASS_NAME",
    "DEFAULT_CLASS_REFERENCE",
    "DEFAULT_COMMA",
    "DEFAULT_CONSTANT",
    "DEFAULT_DOC_COMMENT",
    "DEFAULT_DOC_COMMENT_TAG",
    "DEFAULT_DOC_COMMENT_TAG_VALUE",
    "DEFAULT_DOC_MARKUP",
    "DEFAULT_DOT",
    "DEFAULT_ENTITY",
    "DEFAULT_FUNCTION_CALL",
    "DEFAULT_FUNCTION_DECLARATION",
    "DEFAULT_GLOBAL_VARIABLE",
    "DEFAULT_HIGHLIGHTED_REFERENCE",
    "DEFAULT_IDENTIFIER",
    "DEFAULT_INSTANCE_FIELD",
    "DEFAULT_INSTANCE_METHOD",
    "DEFAULT_INTERFACE_NAME",
    "DEFAULT_INVALID_STRING_ESCAPE",
    "DEFAULT_KEYWORD",
    "DEFAULT_LABEL",
    "DEFAULT_LINE_COMMENT",
    "DEFAULT_LOCAL_VARIABLE",
    "DEFAULT_METADATA",
    "DEFAULT_NUMBER",
    "DEFAULT_OPERATION_SIGN",
    "DEFAULT_PARAMETER",
    "DEFAULT_PARENTHS",
    "DEFAULT_PREDEFINED_SYMBOL",
    "DEFAULT_REASSIGNED_LOCAL_VARIABLE",
    "DEFAULT_REASSIGNED_PARAMETER",
    "DEFAULT_SEMICOLON",
    "DEFAULT_STATIC_FIELD",
    "DEFAULT_STATIC_METHOD",
    "DEFAULT_STRING",
    "DEFAULT_TAG",
    "DEFAULT_TEMPLATE_LANGUAGE_COLOR",
    "DEFAULT_VALID_STRING_ESCAPE",
)

# Java external TextAttributesKey names (JavaHighlightingColors).
JAVA_ATTRIBUTE_IDS: tuple[str, ...] = (
    "ABSTRACT_CLASS_NAME_ATTRIBUTES",
    "ABSTRACT_METHOD_ATTRIBUTES",
    "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES",
    "ANNOTATION_NAME_ATTRIBUTES",
    "ANONYMOUS_CLASS_NAME_ATTRIBUTES",
    "CLASS_NAME_ATTRIBUTES",
    "CONSTRUCTOR_CALL_ATTRIBUTES",
    "CONSTRUCTOR_DECLARATION_ATTRIBUTES",
    "DOC_COMMENT_TAG_VALUE",
    "ENUM_NAME_ATTRIBUTES",
    "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES",
    "INHERITED_METHOD_ATTRIBUTES",
    "INSTANCE_FIELD_ATTRIBUTES",
    "INSTANCE_FINAL_FIELD_ATTRIBUTES",
    "INTERFACE_NAME_ATTRIBUTES",
    "JAVA_BLOCK_COMMENT",
    "JAVA_BRACES",
    "JAVA_BRACKETS",
    "JAVA_COMMA",
    "JAVA_DOC_COMMENT",
    "JAVA_DOC_MARKUP",
    "JAVA_DOC_TAG",
    "JAVA_DOT",
    "JAVA_INVALID_STRING_ESCAPE",
    "JAVA_KEYWORD",
    "JAVA_LINE_COMMENT",
    "JAVA_NUMBER",
    "JAVA_OPERATION_SIGN",
    "JAVA_PARENTH",
    "JAVA_SEMICOLON",
    "JAVA_STRING",
    "JAVA_VALID_STRING_ESCAPE",
    "LAMBDA_PARAMETER_ATTRIBUTES",
    "LOCAL_VARIABLE_ATTRIBUTES",
    "METHOD_CALL_ATTRIBUTES",
    "METHOD_DECLARATION_ATTRIBUTES",
    "MISSORTED_IMPORTS_ATTRIBUTES",
    "PACKAGE_PRIVATE_REFERENCE",
    "PARAMETER_ATTRIBUTES",
    "PRIVATE_REFERENCE",
    "PROTECTED_REFERENCE",
    "PUBLIC_REFERENCE",
    "REASSIGNED_LOCAL_VARIABLE_ATTRIBUTES",
    "REASSIGNED_PARAMETER_ATTRIBUTES",
    "RECORD_COMPONENT_ATTRIBUTES",
    "RECORD_NAME_ATTRIBUTES",
    "STATIC_FIELD_ATTRIBUTES",
    "STATIC_FIELD_IMPORTED_ATTRIBUTES",
    "STATIC_FINAL_FIELD_ATTRIBUTES",
    "STATIC_FINAL_FIELD_IMPORTED_ATTRIBUTES",
    "STATIC_METHOD_ATTRIBUTES",
    "STATIC_METHOD_IMPORTED_ATTRIBUTES",
    "TYPE_PARAMETER_NAME_ATTRIBUTES",
)

# JSON external TextAttributesKey names (JsonSyntaxHighlighterFactory).
JSON_ATTRIBUTE_IDS: tuple[str, ...] = (
    "JSON.BLOCK_COMMENT",
    "JSON.BRACES",
    "JSON.BRACKETS",
    "JSON.COLON",
    "JSON.COMMA",
    "JSON.IDENTIFIER",
    "JSON.INVALID_ESCAPE",
    "JSON.KEYWORD",
    "JSON.LINE_COMMENT",
    "JSON.NUMBER",
    "JSON.PARAMETER",
    "JSON.PROPERTY_KEY",
    "JSON.STRING",
    "JSON.VALID_ESCAPE",
)

# Python external TextAttributesKey names (PyCharm OSS PyHighlighter).
PYTHON_ATTRIBUTE_IDS: tuple[str, ...] = (
    "PY.ANNOTATION",
    "PY.BRACES",
    "PY.BRACKETS",
    "PY.BUILTIN_NAME",
    "PY.CLASS_DEFINITION",
    "PY.COMMA",
    "PY.DECORATOR",
    "PY.DOC_COMMENT",
    "PY.DOC_COMMENT_TAG",
    "PY.DOT",
    "PY.FSTRING_FORMAT_SPEC_NUMBER",
    "PY.FSTRING_FORMAT_SPEC_SPECIAL_CHAR",
    "PY.FSTRING_FRAGMENT_BRACES",
    "PY.FSTRING_FRAGMENT_COLON",
    "PY.FSTRING_FRAGMENT_TYPE_CONVERSION",
    "PY.FUNC_DEFINITION",
    "PY.FUNCTION_CALL",
    "PY.INVALID_STRING_ESCAPE",
    "PY.KEYWORD",
    "PY.KEYWORD_ARGUMENT",
    "PY.LINE_COMMENT",
    "PY.LOCAL_VARIABLE",
    "PY.METHOD_CALL",
    "PY.NESTED_FUNC_DEFINITION",
    "PY.NUMBER",
    "PY.OPERATION_SIGN",
    "PY.PARAMETER",
    "PY.PARENTHS",
    "PY.PREDEFINED_DEFINITION",
    "PY.PREDEFINED_USAGE",
    "PY.SELF_PARAMETER",
    "PY.STRING.B",
    "PY.STRING.U",
    "PY.TYPE_PARAMETER",
    "PY.VALID_STRING_ESCAPE",
)

# Zed syntax roles with no confidently-enumerable IntelliJ key at all and no
# sensible platform DEFAULT to fall back to. They are intentionally not emitted;
# the parent scheme's default applies instead of a guessed id.
#
# Roles whose colour has no dedicated key but a reasonable platform DEFAULT *do*
# have one and are therefore mapped above (for example ``link_text`` ->
# ``DEFAULT_HIGHLIGHTED_REFERENCE``). ``diff.minus`` / ``diff.plus`` are omitted
# here because they belong to the diff/VCS ticket (04c).
UNRESOLVED_ROLE_FALLBACKS: tuple[str, ...] = (
    # Markdown / prose styling (italic / bold emphasis).
    "emphasis",
    "emphasis.strong",
    # No dedicated boolean-literal key in any target language.
    "boolean",
    # Prose heading role (markdown); no IntelliJ heading key.
    "title",
    # Annotation-in-comment severities (todo / fixme / note / warning / error):
    # distinct Zed colours with no IntelliJ comment attribute.
    "comment.todo",
    "comment.warning",
    "comment.error",
    "comment.hint",
    "comment.note",
    # Character literals have no dedicated key (char literal uses the string key).
    "character",
    # Debug keyword is red upstream; there is no debug-keyword attribute.
    "keyword.debug",
    # String sub-roles with no dedicated IntelliJ key (regex/path/url/symbol).
    "string.regex",
    "string.regexp",
    "string.special",
    "string.special.path",
    "string.special.symbol",
    "string.special.url",
    # Preprocessor teal has no IntelliJ preprocessor attribute.
    "preproc",
    # Markup sub-roles without a distinct attribute beyond DEFAULT_TAG/ATTRIBUTE.
    "tag.delimiter",
    "tag.doctype",
    # List markers have no dedicated attribute.
    "punctuation.list_marker",
)

# Zed font_weight/font_style -> IntelliJ FONT_TYPE enum (0 plain, 1 bold,
# 2 italic, 3 bold+italic). Descriptive; the generator derives this per role.
FONT_TYPE_MAP: dict[tuple[str | None, int | None], int] = {
    (None, None): 0,
    (None, 700): 1,
    ("italic", None): 2,
    ("italic", 700): 3,
}

# Zed syntax key -> tuple of IntelliJ attribute ids. Where an id is shared by
# several roles the first listed wins (generator dedupes by id).
SYNTAX_MAP: dict[str, tuple[str, ...]] = {
    # ------------------------------------------------------------------ #
    # Comments and documentation
    # ------------------------------------------------------------------ #
    "comment": (
        "DEFAULT_LINE_COMMENT",
        "DEFAULT_BLOCK_COMMENT",
        "JAVA_LINE_COMMENT",
        "JAVA_BLOCK_COMMENT",
        "KOTLIN_LINE_COMMENT",
        "KOTLIN_BLOCK_COMMENT",
        "PY.LINE_COMMENT",
        "JSON.LINE_COMMENT",
        "JSON.BLOCK_COMMENT",
        "JS.LINE_COMMENT",
        "JS.BLOCK_COMMENT",
        "TS.LINE_COMMENT",
        "TS.BLOCK_COMMENT",
    ),
    "comment.doc": (
        "DEFAULT_DOC_COMMENT",
        "DEFAULT_DOC_MARKUP",
        "DEFAULT_DOC_COMMENT_TAG",
        "DEFAULT_DOC_COMMENT_TAG_VALUE",
        "JAVA_DOC_COMMENT",
        "JAVA_DOC_TAG",
        "JAVA_DOC_MARKUP",
        "DOC_COMMENT_TAG_VALUE",
        "KOTLIN_DOC_COMMENT",
        "KDOC_TAG_NAME",
        "PY.DOC_COMMENT_TAG",
        "JS.DOC_COMMENT",
        "JS.DOC_TAG",
        "JS.DOC_TAG_NAMEPATH",
        "JS.DOC_TYPE",
        "TS.DOC_COMMENT",
        "TS.DOC_TAG",
        "TS.DOC_TAG_NAMEPATH",
        "TS.DOC_TYPE",
    ),
    "comment.documentation": (
        "KOTLIN_DOC_COMMENT",
        "JS.DOC_COMMENT",
        "TS.DOC_COMMENT",
    ),
    "predoc": (
        "DEFAULT_DOC_MARKUP",
        "JAVA_DOC_MARKUP",
    ),
    # Python docstrings are triple-quoted strings upstream, so they take the
    # string-family colour rather than the comment colour.
    "string.doc": ("PY.DOC_COMMENT",),
    "string.documentation": ("PY.DOC_COMMENT",),
    # ------------------------------------------------------------------ #
    # Keywords
    # ------------------------------------------------------------------ #
    "keyword": (
        "DEFAULT_KEYWORD",
        "JAVA_KEYWORD",
        "KOTLIN_KEYWORD",
        "KOTLIN_KEYWORD_VAL",
        "KOTLIN_KEYWORD_VAR",
        "PY.KEYWORD",
        "JSON.KEYWORD",
        "JS.KEYWORD",
        "TS.KEYWORD",
    ),
    # Zed keyword.operator is the same cyan as operator/punctuation.
    "keyword.operator": (
        "DEFAULT_OPERATION_SIGN",
        "JAVA_OPERATION_SIGN",
        "KOTLIN_OPERATION_SIGN",
        "PY.OPERATION_SIGN",
        "JS.OPERATION_SIGN",
        "TS.OPERATION_SIGN",
    ),
    # ------------------------------------------------------------------ #
    # Numbers and constants
    # ------------------------------------------------------------------ #
    "number": (
        "DEFAULT_NUMBER",
        "JAVA_NUMBER",
        "KOTLIN_NUMBER",
        "PY.NUMBER",
        "JSON.NUMBER",
        "JS.NUMBER",
        "TS.NUMBER",
    ),
    "constant": ("DEFAULT_CONSTANT",),
    "constant.builtin": ("DEFAULT_CONSTANT",),
    # Macro names are purple upstream, like metadata / annotations.
    "constant.macro": ("DEFAULT_METADATA",),
    # ------------------------------------------------------------------ #
    # Strings and escapes
    # ------------------------------------------------------------------ #
    "string": (
        "DEFAULT_STRING",
        "JAVA_STRING",
        "KOTLIN_STRING",
        "PY.STRING.B",
        "PY.STRING.U",
        "JSON.STRING",
        "JS.STRING",
        "TS.STRING",
    ),
    # Zed character.special carries the escape purple upstream.
    "character.special": (
        "DEFAULT_VALID_STRING_ESCAPE",
        "DEFAULT_INVALID_STRING_ESCAPE",
        "JAVA_VALID_STRING_ESCAPE",
        "JAVA_INVALID_STRING_ESCAPE",
        "KOTLIN_STRING_ESCAPE",
        "KOTLIN_INVALID_STRING_ESCAPE",
        "PY.VALID_STRING_ESCAPE",
        "PY.INVALID_STRING_ESCAPE",
        "JSON.VALID_ESCAPE",
        "JSON.INVALID_ESCAPE",
        "JS.VALID_STRING_ESCAPE",
        "JS.INVALID_STRING_ESCAPE",
        "TS.VALID_STRING_ESCAPE",
        "TS.INVALID_STRING_ESCAPE",
    ),
    # ------------------------------------------------------------------ #
    # Functions
    # ------------------------------------------------------------------ #
    "function": (
        "DEFAULT_FUNCTION_DECLARATION",
        "METHOD_DECLARATION_ATTRIBUTES",
        "KOTLIN_FUNCTION_DECLARATION",
        "PY.FUNC_DEFINITION",
        "PY.NESTED_FUNC_DEFINITION",
        "JS.FUNCTION_ARROW",
        "TS.FUNCTION_ARROW",
    ),
    "function.call": (
        "DEFAULT_FUNCTION_CALL",
        "METHOD_CALL_ATTRIBUTES",
        "KOTLIN_FUNCTION_CALL",
        "KOTLIN_PACKAGE_FUNCTION_CALL",
        "KOTLIN_DYNAMIC_FUNCTION_CALL",
        "KOTLIN_SUSPEND_FUNCTION_CALL",
        "PY.FUNCTION_CALL",
        "PY.METHOD_CALL",
        "JS.GLOBAL_FUNCTION",
        "JS.LOCAL_FUNCTION",
        "TS.GLOBAL_FUNCTION",
        "TS.LOCAL_FUNCTION",
    ),
    "function.method": ("STATIC_METHOD_ATTRIBUTES",),
    "function.method.call": (
        "KOTLIN_EXTENSION_FUNCTION_CALL",
        "JS.STATIC_MEMBER_FUNCTION",
        "JS.INSTANCE_MEMBER_FUNCTION",
        "TS.STATIC_MEMBER_FUNCTION",
        "TS.INSTANCE_MEMBER_FUNCTION",
    ),
    # Python builtin functions are blue upstream (function.builtin), so the
    # builtin key takes the function colour rather than the variable one.
    "function.builtin": ("PY.BUILTIN_NAME",),
    # Decorators / annotations / metadata are purple upstream.
    "function.decorator": (
        "DEFAULT_METADATA",
        "PY.DECORATOR",
        "PY.ANNOTATION",
        "JS.DECORATOR",
        "TS.DECORATOR",
        "KOTLIN_ANNOTATION",
        "KOTLIN_BUILTIN_ANNOTATION",
    ),
    "function.macro": ("DEFAULT_METADATA",),
    # Constructors are red upstream, distinct from the function blue.
    "constructor": (
        "CONSTRUCTOR_CALL_ATTRIBUTES",
        "CONSTRUCTOR_DECLARATION_ATTRIBUTES",
        "KOTLIN_CONSTRUCTOR",
    ),
    # ------------------------------------------------------------------ #
    # Types and enums
    # ------------------------------------------------------------------ #
    "type.class.definition": (
        "CLASS_NAME_ATTRIBUTES",
        "ANONYMOUS_CLASS_NAME_ATTRIBUTES",
        "ABSTRACT_CLASS_NAME_ATTRIBUTES",
        "KOTLIN_CLASS",
    ),
    "type.interface": (
        "INTERFACE_NAME_ATTRIBUTES",
        "KOTLIN_TRAIT",
    ),
    "type.builtin": (
        "JS.PRIMITIVE.TYPE",
        "TS.PRIMITIVE.TYPES",
    ),
    "type.super": ("DEFAULT_CLASS_REFERENCE",),
    "type.definition": (
        "JS.TYPE_ALIAS",
        "TS.TYPE.ALIAS",
        "KOTLIN_TYPE_ALIAS",
    ),
    "enum": (
        "ENUM_NAME_ATTRIBUTES",
        "KOTLIN_ENUM",
        "KOTLIN_ENUM_ENTRY",
    ),
    "type": (
        "DEFAULT_CLASS_NAME",
        "DEFAULT_INTERFACE_NAME",
        "DEFAULT_CLASS_REFERENCE",
        "JS.CLASS",
        "JS.INTERFACE",
        "TS.CLASS",
        "TS.INTERFACE",
        "PY.CLASS_DEFINITION",
        "KOTLIN_DATA_CLASS",
        "KOTLIN_DATA_OBJECT",
        "KOTLIN_OBJECT",
    ),
    # ------------------------------------------------------------------ #
    # Variables, fields, parameters, labels
    # ------------------------------------------------------------------ #
    "variable": (
        "DEFAULT_LOCAL_VARIABLE",
        "DEFAULT_GLOBAL_VARIABLE",
        "LOCAL_VARIABLE_ATTRIBUTES",
        "KOTLIN_LOCAL_VARIABLE",
        "KOTLIN_MUTABLE_VARIABLE",
        "PY.LOCAL_VARIABLE",
        "JS.LOCAL_VARIABLE",
        "TS.LOCAL_VARIABLE",
        "JSON.IDENTIFIER",
    ),
    # Members / fields / properties share the base foreground upstream.
    "variable.member": (
        "DEFAULT_INSTANCE_FIELD",
        "DEFAULT_STATIC_FIELD",
        "INSTANCE_FIELD_ATTRIBUTES",
        "STATIC_FIELD_ATTRIBUTES",
        "INSTANCE_FINAL_FIELD_ATTRIBUTES",
        "STATIC_FINAL_FIELD_ATTRIBUTES",
        "KOTLIN_INSTANCE_PROPERTY",
        "KOTLIN_PACKAGE_PROPERTY",
        "KOTLIN_BACKING_FIELD_VARIABLE",
        "KOTLIN_SYNTHETIC_EXTENSION_PROPERTY",
        "KOTLIN_EXTENSION_PROPERTY",
        "KOTLIN_DYNAMIC_PROPERTY_CALL",
        "KOTLIN_INSTANCE_PROPERTY_CUSTOM_PROPERTY_DECLARATION",
        "KOTLIN_PACKAGE_PROPERTY_CUSTOM_PROPERTY_DECLARATION",
        "JS.INSTANCE_MEMBER_VARIABLE",
        "JS.STATIC_MEMBER_VARIABLE",
        "TS.INSTANCE_MEMBER_VARIABLE",
        "TS.STATIC_MEMBER_VARIABLE",
    ),
    # JSON object keys.
    "property": ("JSON.PROPERTY_KEY",),
    # Builtin variables (True / self / predefined) are red upstream.
    "variable.builtin": (
        "DEFAULT_PREDEFINED_SYMBOL",
        "PY.PREDEFINED_USAGE",
        "PY.PREDEFINED_DEFINITION",
    ),
    # Special variables (self, smart casts) are red upstream.
    "variable.special": (
        "PY.SELF_PARAMETER",
        "KOTLIN_SMART_CAST_RECEIVER",
        "KOTLIN_SMART_CAST_VALUE",
    ),
    "parameter": (
        "DEFAULT_PARAMETER",
        "PARAMETER_ATTRIBUTES",
        "LAMBDA_PARAMETER_ATTRIBUTES",
        "KOTLIN_PARAMETER",
        "KOTLIN_CLOSURE_DEFAULT_PARAMETER",
        "KOTLIN_CONTEXT_ARGUMENT",
        "KOTLIN_NAMED_ARGUMENT",
        "PY.PARAMETER",
        "PY.TYPE_PARAMETER",
        "PY.KEYWORD_ARGUMENT",
        "JS.PARAMETER",
        "TS.PARAMETER",
        "JSON.PARAMETER",
    ),
    # Zed models parameter as a variable role too; shares the same ids.
    "variable.parameter": (
        "DEFAULT_PARAMETER",
        "PARAMETER_ATTRIBUTES",
        "KOTLIN_PARAMETER",
        "PY.PARAMETER",
        "JS.PARAMETER",
        "TS.PARAMETER",
    ),
    "label": (
        "DEFAULT_LABEL",
        "KOTLIN_LABEL",
        "JS.LABEL",
        "TS.LABEL",
    ),
    # ------------------------------------------------------------------ #
    # Punctuation and operators
    # ------------------------------------------------------------------ #
    "punctuation.bracket": (
        "DEFAULT_PARENTHS",
        "DEFAULT_BRACKETS",
        "DEFAULT_BRACES",
        "JAVA_PARENTH",
        "JAVA_BRACKETS",
        "JAVA_BRACES",
        "KOTLIN_PARENTHESIS",
        "KOTLIN_BRACKETS",
        "KOTLIN_BRACES",
        "PY.PARENTHS",
        "PY.BRACKETS",
        "PY.BRACES",
        "JS.PARENTHS",
        "JS.BRACKETS",
        "JS.BRACES",
        "TS.PARENTHS",
        "TS.BRACKETS",
        "TS.BRACES",
        "JSON.BRACKETS",
        "JSON.BRACES",
    ),
    "punctuation.delimiter": (
        "DEFAULT_COMMA",
        "DEFAULT_SEMICOLON",
        "DEFAULT_DOT",
        "JAVA_COMMA",
        "JAVA_SEMICOLON",
        "JAVA_DOT",
        "KOTLIN_COMMA",
        "KOTLIN_SEMICOLON",
        "KOTLIN_DOT",
        "KOTLIN_COLON",
        "PY.COMMA",
        "PY.DOT",
        "JS.COMMA",
        "JS.SEMICOLON",
        "JS.DOT",
        "TS.COMMA",
        "TS.SEMICOLON",
        "TS.DOT",
        "JSON.COMMA",
        "JSON.COLON",
    ),
    # Special punctuation (Kotlin double-colon / arrow / nullability marks,
    # template-literal delimiters) has no platform default of its own.
    "punctuation.special": (
        "KOTLIN_DOUBLE_COLON",
        "KOTLIN_ARROW",
        "KOTLIN_QUEST",
        "KOTLIN_SAFE_ACCESS",
        "KOTLIN_EXCLEXCL",
        "KOTLIN_AMPERSAND",
        "JS.TEMPLATE_LITERAL_PLACEHOLDER_DELIMITERS",
        "TS.TEMPLATE_LITERAL_PLACEHOLDER_DELIMITERS",
    ),
    # Zed operator and keyword.operator are the cyan operator family.
    "operator": (
        "DEFAULT_OPERATION_SIGN",
        "JAVA_OPERATION_SIGN",
        "KOTLIN_OPERATION_SIGN",
        "PY.OPERATION_SIGN",
        "JS.OPERATION_SIGN",
        "TS.OPERATION_SIGN",
    ),
    # ------------------------------------------------------------------ #
    # Tags and attributes (markup)
    # ------------------------------------------------------------------ #
    "tag": ("DEFAULT_TAG",),
    "tag.attribute": ("DEFAULT_ATTRIBUTE",),
    # Zed `attribute` is the HTML/XML attribute-name role.
    "attribute": ("DEFAULT_ATTRIBUTE",),
    # ------------------------------------------------------------------ #
    # Fallback routing to platform defaults
    # ------------------------------------------------------------------ #
    # Links have no dedicated language key, but a platform highlighted-reference
    # default exists; KDOC links also take the link colour.
    "link_text": ("KDOC_LINK", "DEFAULT_HIGHLIGHTED_REFERENCE"),
    "link_uri": ("DEFAULT_HIGHLIGHTED_REFERENCE",),
    # Embedded languages use the platform template-language colour.
    "embedded": ("DEFAULT_TEMPLATE_LANGUAGE_COLOR",),
    # Structural / meta roles with no dedicated key fall back to the plain
    # identifier colour rather than being dropped.
    "namespace": ("DEFAULT_IDENTIFIER",),
    "module": ("DEFAULT_IDENTIFIER",),
    "concept": ("DEFAULT_IDENTIFIER",),
    "variant": ("DEFAULT_IDENTIFIER",),
    "symbol": ("DEFAULT_IDENTIFIER",),
    "primary": ("DEFAULT_IDENTIFIER",),
    "parent": ("DEFAULT_IDENTIFIER",),
}
