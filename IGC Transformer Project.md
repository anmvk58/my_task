# IGC Transformer Project.

## Purpose

The main idea to create this transformation was to allow Users to work with Infosphere Glossary Catalog easiest way.

## Terms And Definitions

| **Acronym** | **Definition** |
| --- | --- |
| IGC | Infosphere Glossary Catalog |
| IGCTransformer | Transformation project to transform Input XML file to Output XML file and back |
| Input XML file | File we export from specifically designed EXCEL file |
| Output XML file | File that follows XML schema for import/export IGC assets |
| Input XML schema | Specifically designed schema that represents IGC assets in simple way |
| Output XML Schema | BGSchema.xsd – standard import/export xml files schema for IGC |
| Forward Transformation | Transformation process that passes data from Input XML file to Output XML file |
| Backward Transformation | Transformation process that passes data from Output XML file to Input XML file |
| IGC assets | The subset of objects that Infosphere Glossary Catalog can work with. Category, Term, Label, Custom Attribute, Policy, Rule, Assigned Assets (glossary assets that can be assigned to Term). |

## Overall Process Workflow Description

Workflow of the process contains two main components:

1. EXCEL File that allows End users to work with IGC assets easiest way.
2. IGCTransformer application that transform data between Input XML file and Output XML file.

IGC works with many types of objects (assets). Detailed information about information assets that ICG can work with you can read in the Infosphere Information Server documentation. But key object from Glossary users is Term. According to BGSchema.xsd schema structure of Term element contains complicated hierarchy. Simple child elements of course can be putted easily but when child element contains multichoice structure it is impossible to interpret this structure as tabular data. How to solve this problem? Let us divide Term structure to several parts:

- Simple child element part
- Complex child element part

Simple child element part can be represented by table (list of attributes + list of simple child elements).

For complex child element part let us create set of EXCEL sheet. Complex child elements are Term mappings (set of assets that can be assigned to Term: Logical Attribute/Table, Physical Attribute/Table, physical DB structure table or attribute, Data Stage jobs.). All of these assets have their own attributes so it is impossible to create one common EXCEL sheet.

There are two main flows:

1. Export xml file from IGC.
 Transform IGC format XML file into EXCEL format xml file.
 Load EXCEL format xml file into EXCEL template.
 Use EXCEL file with loaded content to edit, add new assets.
2. Export EXCEL format xml file from EXCEL.
 Transform exported file to IGC format xml file.
 Import transformed file into IGC.

## EXCEL template and corresponding xml Schema (xsd) file.

In this we investigate more detailed EXCEL part of the project.
 Start with xml schema file.
 Root element of the schema is &quot;input&quot;

Possible (optional) child elements of the root element can be:

- customAttributesDefinitions – reflect the same element in the IGC format xml
- categories – reflect the same section of the IGC format xml
- terms – reflect the same section of the IGC format xml (except assignedAssets)
- policies – reflect the same section of the IGC format xml
- rules – reflect the same section of the IGC format xml
- labelDefinitions – reflect the same section of the IGC format xml
- termsToSOR – Logical Atomic Model (SoR) mappings (assigned to term assets)
- termsToDM – Logical Data Mart/Interface model mappings
- termsToPhysicalSOR – Physical Atomic Model (SoR) mappings
- termsToPhysicalDM – Physical Data Mart/Interface mappings
- termsToJobs – Data Stage jobs mappings
- termsToImplAssest – RDBMS tables and attributes mappings
- assetReferences – old section not used now.

###

### Custom attribute definitions section

Let talk more detailed about custom attributes section.

CustomAttributesDefinitions elements can contain zero or more elements &quot;customAttributeDef&quot;.
 customAttributeDef element contains next attributes:

- rid – IGC system internal identifier. String attribute with length of 64 symbols.
- name
- description
- attributeType – string enumeration (TEXT, DATE, BOOLEAN, NUMBER, PREDEFINED\_VALUES, REFERENCE)
- multipleValues – Boolean flag. Indicates that this attribute can have multiple values or not.

There are two more child elements for attribute def:

- validValues – optional element with list of valid values divided by &quot;,&quot; and surrounded by &quot;()&quot;.
 This is a trick to put attributes with multiple values in the table instead to create one more table.
- appliesTo – optional element with list of values (TERM, CATEGORY, POLICY, RULE) divided by &quot;,&quot; surrounded by &quot;()&quot;

Last two elements have inside one attribute &quot;value&quot; as described above attribute value is a string with multiple values divided by &quot;,&quot; and surrounded by &quot;()&quot;. We will see many attributes like these in the future. In the xml Schema file, I have specifically created Type – &quot;inputValueType&quot; with one attribute &quot;value&quot;.

### Categories section

Let us investigate more detailed categories section.

Optional element &quot;categories&quot; contains zero or more &quot;category&quot; elements.
 Every &quot;category&quot; element contains next attributes:

- rid – IGC system internal identifier.
- name
- shortDescription
- longDescription

and next optional child elements:

- labels – list of label names divided by &quot;,&quot; surrounded by &quot;()&quot;. This element of &quot;inputValueType&quot; type
- stewards – list of user names (IGC steward users) divided by &quot;,&quot; surrounded by &quot;()&quot;. This element also &quot;inputValueType&quot;
- parentCategory – because IGC has categories hierarchy this element identifies parent categories hierarchy. This element of &quot;glossaryAssetRefDef&quot; type and contains two attributes:
  - rid – identifier of parent category (optional if you create new category this attribute must be empty this attribute filled after you export information from IGC).
  - Identity – string attribute reflects categories hierarchy divided by &quot;\&gt;\&gt;&quot;.
 Ex. Category1\&gt;\&gt;Category2\&gt;\&gt;Category3. Where Category1 is the topmost category and Category3 is the lowest category in hierarchy.

### Terms section

More detailed about terms section.

Terms element contains zero or more &quot;term&quot; child elements.

Every &quot;term&quot; element contains attributes:

- rid
- name
- shortDescription
- longDescription
- status – string enumeration (CANDIDATE, ACCEPTED, STANDARD, DEPRECATED)
- usage
- example
- abbreviation
- additionalAbbreviation
- type – string enumeration (PRIMARY, SECONDARY, NONE)
- isModifier – Boolean flag (TRUE, FALSE)
- Formula – this is an example how to put custom attribute in the list of attributes. Custom attribute starts with Capital letter. Any whitespace in the name replaced by &quot;\_&quot; sumbol.
- Decomposition – another custom attribute
- External\_Document\_Reference - one more custom attribute
- Index – one more custom attribute

And next child elements:

- labels – optional element. list of label names divided by &quot;,&quot; and surrounded by &quot;()&quot;
- stewards – optional element. List of IGC stewards divided by &quot;,&quot; surrounded by &quot;()&quot;
- parentCategory – mandatory attribute. Every term must belong to parent category.
 the structure of &quot;parentCategory&quot; element described in the categories section.
- isATypeOf – optional element. This element is not used now. But element attribute &quot;value&quot; should contain list of &quot;full term path&quot; values divided by &quot;,&quot; and surrounded by &quot;()&quot;.
 Full term path – full hierarchy of term categories followed by term name. All values divided by &quot;\&gt;\&gt;&quot;.

I will come back to terms section when we will talk about terms transformation.

### Policies section

Element &quot;policies&quot; contains zero or more &quot;policy&quot; elements.

Every &quot;policy&quot; element contains next attributes:

- rid
- name
- shortDescription
- longDescription

and next child elements:

- labels - optional
- stewards – optional
- parentPolicy – optional. Element of &quot;glossaryAssetRef&quot; type. Contains two attributes: rid and identity.
- referencedRules – optional element. Element contains list of &quot;full path to rule&quot; values divided by &quot;,&quot; and surrounded by &quot;()&quot;.

### Rules section

Element &quot;rules&quot; contains zero or more &quot;rule&quot; elements.

Every &quot;rule&quot; element contains next attributes:

- rid
- name
- shortDescritpion
- longDescription

and next child elements:

- labels – optional
- stewards – optional
- referencedByPolicies – optional. List of &quot;full path to policy&quot; divided by &quot;,&quot; and surrounded by &quot;()&quot;. Full path to policy contains parent policies hierarchy and policy name. All elements in path divided by &quot;\&gt;\&gt;&quot;.

### Labels section

Element &quot;labelDefinitions&quot; contains zero or more &quot;labelDefinition&quot; elements.

Every &quot;labelDefinition&quot; element contains next attributes:

- rid
- name
- description

### Mapping sections &quot;termsToSOR&quot;, &quot;termsToDM&quot;, &quot;termsToPhysicalSOR&quot;, &quot;termsToPhysicalDM&quot;

These sections divided to support parallel mapping to Atomic and DM models.

The structure of these section is common. Element &quot;termsToSOR&quot;, &quot;termsToDM&quot;, &quot;termsToPhysicalSOR&quot;, &quot;termsToPhysicalDM&quot; contains zero or more elements &quot;termToSORRef&quot;, &quot;termToDMRef&quot;, &quot;termToPSORRef&quot;, &quot;termToPDMRef&quot;.

Every &quot;Ref&quot; element contains next attributes:

- termCategory – mandatory attribute. Contains categories hierarchy for term divided by &quot;\&gt;\&gt;&quot;
- termName – mandatory attribute.
- entityName – mandatory attribute. Name of the logical entity in the mapping.
- attributeName – optional attribute. Name of the entity attribute.
- entityPath – mandatory attribute. Full path to the entity (packages hierarchy) divided by &quot;\&gt;\&gt;&quot;
- namespace – mandatory attribute. When Information Server perform models import every model should contain model namespace. We can have several models imported under the same namespace. And may have the same model imported under different workspaces.

Based on every row in section during transformation we will build Hash Map object.
 Has map is the \&lt;key, object\&gt; pair. To build key for term we will use &quot;termCategory+termName&quot; (in IGC this is alternative unique key for terms), and collect all &quot;attribute::entity::entityPath::namespace&quot; in the list (we may have more than one mapping for one term).

### Section &quot;termsToJobs&quot;

Element &quot;termsToJobs&quot; contains zero or more child elements &quot;termToJobRef&quot;.

Element &quot;termToJobRef&quot; contains next attributes:

- termCategory – full path to term category divided by &quot;\&gt;\&gt;&quot;
- termName
- transformServer – name of the DataStage Server
- transformProject – name of the Transformation DataStage project
- jobname – name of the DataStage job

### Section &quot;termsToImplAsset&quot;

The root element &quot;termsToImplAsset&quot; contains zero or more &quot;termToImplAssetRef&quot; elements.

Every &quot;Ref&quot; element contains next attributes:

- termCategory
- termName
- assetHost – Name or IP address of the Database host
- assetDBName – Database name
- assetDBInstance – optional attribute. Database instance
- assetDBMS – optional attribute. Type of RDMBS.
- assetDBSchema – database schema
- assetDBTable – database table name
- assetDBColumn – table column name

## Infosphere Glossary Catalog schema file

This file exported from IGC and contains all possible elements that IGC can operate with.

Root element of the corresponding xml file is &quot;glossary&quot;.

Let me list the sections current project is working with.

### Section &quot;customAttributesDefinitions&quot;

This is optional section and element &quot;customAttributesDefinitions&quot; contains zero or more &quot;customAttributeDef&quot; elements.

Every &quot;customAttributeDef&quot; contains next attributes:

- rid – internal IGC identifier.
- Name – mandatory
- Description
- attributeType – string attribute restricted with list of values (TEXT, DATE, BOOLEAN, NUMBER, PREDEFINED\_VALUES, REFERENCE)
- multipleValues – Boolean attribute indicates that custom attribute may or may not contains multiple values
- inverseReferenceName – optionl attribute This attribute is not used in our scope

and next child elements:

- validValues – optional element. This element contains zero or more &quot;validValue&quot; elements. Each &quot;validValue&quot; element contains two attributes (value – string, description - string). During transformation from EXCEL format file &quot;value&quot; attribute of input &quot;validValues&quot; element split by &quot;,&quot; and for every splitted token &quot;transformer&quot; creates new &quot;validValue&quot; element and put token to the value attribute
- appliesTo – optional element. Element &quot;appliesTo&quot; contains one or many &quot;classType&quot; elements. Element &quot;classType&quot; contains &quot;value&quot; attribute (string type). During transformation I get &quot;value&quot; attribute of the input &quot;appliesTo&quot; element split it with &quot;,&quot; and for every toke create output &quot;classType&quot; element.
- relatesTo – optionl element. Not used in out scope.

### Section &quot;categories&quot;

Element &quot;categories&quot; is optional. Element &quot;categories&quot; contains zero or more &quot;category&quot; element.

Every &quot;category&quot; element contains next attributes:

- rid – system identifier
- name
- shortDescription
- longDescription
- language – not used

and next child elements:

- customAttributes – optional element. This element contains zero or more &quot;customAttributeValue&quot; elements. Each &quot;customAttributeValue&quot; contains two attributes (customAttribute – name of attribute, and value – value of attribute) and two child elements (attributeValue – value of attribute, customAttributeReferences – not used in our scope). Every test export from IGC have not used &quot;value&quot; attribute, all export use child &quot;attributeValue&quot; element. During transformation I collect list of Custom Attributes and create for each &quot;customAttributeValue&quot; element with child &quot;attributeValue&quot; element.
- labels – contains zero or more &quot;label&quot; child element. Every &quot;label&quot; child element contains &quot;name&quot; attribute. During transformation I get input &quot;labels&quot; element and split its &quot;value&quot; attribute by &quot;,&quot;. For every token I create target &quot;label&quot; element.
- stewards – list of steward users. Element &quot;stewards&quot; contains zero or more &quot;steward&quot; element. Every &quot;steward&quot; element contains two attributes (type – always USER, userName). During transformation I get input &quot;stewards&quot; element split &quot;value&quot; attribute by &quot;,&quot; and for every token create target &quot;steward&quot; element.
- parentCategory – full path to parent category. Element &quot;parentCategory&quot; contains two attributes (rid and identity – path to category divided by &quot;::&quot;)

### Section &quot;terms&quot;

Element &quot;terms&quot; contains zero or more &quot;term&quot; elements.

Element &quot;term&quot; contains next attributes:

- rid
- name
- shortDescription
- longDescription
- status – string enumeration (CANDIDATE, ACCEPTED, STANDARD, DEPRECATED)
- usage
- example
- abbreviation
- additionalAbbreviation
- type – string enumeration (PRIMARY, SECONDARY, NONE)
- isModifier – Boolean

during transformation because input attribute names is the same as target I move attributes from source to target as is (with name and value).

Element &quot;term&quot; contains next child elements:

- customAttributes – the same as &quot;customAttributes&quot; in the &quot;categories&quot; section
- labels – the same as in the &quot;categories&quot; section
- stewards – tha same as in the &quot;categories&quot; section
- parentCategory – Mandatory element. Structure is the same as in the &quot;categories&quot; section.
- isATypeOf – rarely used element. Contains zero or more &quot;termRef&quot; elements. Every element contains &quot;identity&quot; attribute is the &quot;full path to term&quot; divided by &quot;::&quot;. During transformation I get &quot;value&quot; attribute of &quot;isTypeOf&quot; input element, split it by &quot;,&quot; and for every token create &quot;termRef&quot; element and put token to &quot;identoty&quot; attribute (replacing input delimiter &quot;\&gt;\&gt;&quot; to output &quot;::&quot;)
- assignedAssets – most complicated element of this section. This element contains list of term assignments (Logical Entity/Attribute, Physcial Table/Columns, DataStage jobs, Database specifications, tables and columns). To build this target element first of all I build hashtable of all input sections termsToSOR, termsToDm, termsToPSOR, termsToPDM, termsToJobs and termsToImplAssets. Then during working with current term I search through the hashtables for corresponding mappings and depend of the type of asset create corresponding target elements.
