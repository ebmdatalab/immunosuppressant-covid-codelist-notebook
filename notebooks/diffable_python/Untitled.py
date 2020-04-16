# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---



# +

from ebmdatalab import bq
import os
import pandas as pd

# +
# The following is written based on version 1 frm March 27th and 
## is archived at https://web.archive.org/save/https://digital.nhs.uk/coronavirus/shielded-patient-list/methodology/medicines-data

sql = '''
WITH bnf_codes AS (  
  SELECT bnf_code FROM hscic.presentation WHERE 
  (##transplant
  bnf_code LIKE '0802%' OR # the following meds are listed in definition but annex looks like they included all meds in this section
  ##respiratory
  bnf_code LIKE '030302%' OR #BNF leukotriene antagonists
  bnf_code LIKE '0603020T0%' OR #BNF prednisolone
  bnf_code LIKE '030101%' OR #BNF adrenoceptor aganosts
  bnf_code LIKE '0302%' OR #BNF corticosteroids resp
  bnf_code LIKE '0303030B0%' OR #BNF roflumilast 
  bnf_code LIKE '030102%') #BNF antimuscarinin brochodilators
  AND
  (bnf_code NOT LIKE '0802020T0%XAX' OR #BNF tacrolimus mouthwash
  bnf_code NOT LIKE '0301011R0%')
   )
SELECT onj_type, id, bnf_code, nm
FROM ebmdatalab.measures_v2.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY bnf_code, type, id'''

immunosuppressants = bq.cached_read(sql, csv_path=os.path.join('..','data','immunosuppressants.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
immunosuppressants.head(10)
