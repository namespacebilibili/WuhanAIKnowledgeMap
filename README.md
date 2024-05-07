# WuhanAIKnowledgeMap

Project for AI and Sociology 2024

## Preprocess 

In `preprocess.py`:
+ Run `preprocess()` to generate companies related to AI in Wuhan.
+ Run `match_product_to_standard_product()` to match products to standard products and add standard products and industry chain info to the company data.
+ Run `select_company` to select companies that have more than `n` standard products.

In `utils_patent.py`:
+ helper functions related to patent information and patent collaboration information:
+ Run `extract_patent()` to filter AI related patents.
+ Run `evaluate()` to count patent numbers for each unique AI company and evaluate innovation standard.
+ Run `collaborators()` to collect information about patent collaborators.
