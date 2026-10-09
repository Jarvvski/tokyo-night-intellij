"""Syntax mapping: Zed syntax key -> IntelliJ attribute ids (per language).

Filled in by the syntax ticket (03), gated on the Phase 0 attribute-id harvest
(this module's ``*_ATTRIBUTE_IDS`` constants). Never invent an id: if a language
role cannot be confidently enumerated, fall back to a platform DEFAULT attribute
rather than guessing.

Phase 0 harvest (ticket 01): verified IntelliJ ``TextAttributesKey`` *names* only,
no color values copied. Sources are the bundled registration inside the locally
installed IDEs:

* JavaScript / TypeScript - WebStorm 2026.x,
  ``plugins/javascript-plugin/lib/modules/intellij.javascript.psi.impl.jar``:
  - ``com.intellij.lang.javascript.highlighting.JavaScriptHighlightDescriptor``:
    external keys are ``"JS." + descriptorName`` (prefix confirmed from the
    ``makeConcatWithConstants`` recipe ``JS.\\u0001``); six descriptors override
    their suffix explicitly: PARENTHESES->PARENTHS,
    BAD_CHARACTER->BADCHARACTER, PRIMITIVE_TYPE->PRIMITIVE.TYPE,
    EXPORTED_VARIABLE/FUNCTION/CLASS->EXPORTED.VARIABLE/FUNCTION/CLASS.
  - ``com.intellij.lang.javascript.highlighting.TypeScriptHighlighter``:
    external keys are literal ``TS.*`` strings.
* Kotlin - IDEA-bundled Kotlin plugin,
  ``plugins/Kotlin/lib/kotlin-plugin-shared.jar``,
  ``org.jetbrains.kotlin.idea.highlighter.KotlinHighlightingColors``:
  external keys are literal ``KOTLIN_*`` / ``KDOC_*`` names (cross-checked against
  the bundled ``intellij.kotlin.base.resources.jar:/colorScheme/Darcula_Kotlin.xml``).

Aliased-only TS descriptors are intentionally omitted because they resolve to an
existing key rather than registering a standalone external name: ``TS_ENUM``,
``TS_ENUM_MEMBER`` and ``TS_TYPE_PARAMETER`` (all created via ``getMappedKey``).
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

# Zed syntax roles with no confidently-enumerable JS/TS/Kotlin attribute key.
# Ticket 03 must route these to a platform DEFAULT attribute instead of guessing.
UNRESOLVED_ROLE_FALLBACKS: tuple[str, ...] = (
    # Markdown / prose roles (no code equivalent).
    "emphasis",
    "emphasis.strong",
    # Markup roles owned by the HTML/XML plugin, not the JS/TS/Kotlin highlighters.
    "tag",
    "tag.attribute",
    "tag.delimiter",
    "tag.doctype",
    # Link / preprocessor / macro roles with no JS/TS/Kotlin key.
    "link_text",
    "link_uri",
    "preproc",
    "function.macro",
    "constant.macro",
    # Structural / meta roles with no dedicated key.
    "namespace",
    "module",
    "embedded",
    "primary",
    "parent",
    "concept",
    "variant",
    "symbol",
    # Punctuation subroles without a distinct key.
    "punctuation.list_marker",
    "punctuation.special",
    "punctuation.delimiter",
    # String subroles without a distinct key.
    "string.doc",
    "string.documentation",
    "string.special.path",
    "string.special.url",
    "string.special.symbol",
)

# Zed font_weight/font_style -> IntelliJ FONT_TYPE enum (0 plain, 1 bold,
# 2 italic, 3 bold+italic).
FONT_TYPE_MAP: dict[tuple[str | None, int | None], int] = {}

# Zed syntax key -> tuple of IntelliJ attribute ids.
SYNTAX_MAP: dict[str, tuple[str, ...]] = {}
