# Commenting style for ASN.1 Doxygen filter

## 1. OID name/Module name
Use the `@namespace` tag to mention an OID name. This helps the filter to group
the rest of the structures under this "namespace". For example:
```asn
-- @namespace OidName
```

Prefer to not use any special characters in OID name.

## 2. Comment Section
A comment section should **ALWAYS** start with three hyphens (`---`) followed
by the rest of the comment block. There is no indicator for ending of a comment
block.

### 2.1 Structure Description
Use tag `@brief` to briefly describe the function of a structure. For example:
```asn
-- @brief This is the first line of comment.
--        Note that the second line of comment has the same hanging indentation
--        as the first line.
```

### 2.2 Structure tag
Use `@class` tag to specify structure name. For example:
```asn
-- @class StructureName
```

### 2.3 Parameter description
ASN.1 strucutures may contains parameters. To describe them, use the `@param`
tag. For example:
```asn
-- @param parameterName This is the first line that describes the parameter's
--                      role in a structure. Note that this second line of
--                      comment has the same hanging indentation as the first
--                      line.
```

### 2.4 Refer Structures from other files
Some structures might contain other structures that are defined in other files.
It is also possible that a structure in another file might be relevant to the
structure you are commenting. In these cases, use the `@see` tag to refer them.
For example:
```asn
-- @see SomeStructureFromAnotherFile, OneMore, AnotherOne
```

## 3. Tying everything together
Below is a sample ASN.1 structure with comments for guidance on how each
structure should look like in an for the ASN.1 filter to work properly.
```asn
---
-- @brief This is the first line of comment.
--        Note that the second line of comment has the same hanging indentation
--        as the first line.
-- @class StructureName
-- @param parameterNameOne   This is the first line that describes the
--                           parameter's role in a structure. Note that this
--                           second line of comment has the same hanging
--                           indentation as the first line.
-- @param parameterNameTwo   This is the first line that describes the
--                           parameter's role in a structure. Note that this
--                           second line of comment has the same hanging
--                           indentation as the first line.
-- @param parameterNameThree This is the first line that describes the
--                           parameter's role in a structure. Note that this
--                           second line of comment has the same hanging
--                           indentation as the first line.
-- @see SomeStructureFromAnotherFile, OneMore, AnotherOne
StructureName ::= StructureType {
    parameterNameOne SomeStructureFromAnotherFile,
    parameterNameTwo OneMore,
    parameterNameThree AnotherOne
}
```

Please refer the [sample](sample.asn) file to see how a complete file should
look for this ASN.1 filter to work properly.
