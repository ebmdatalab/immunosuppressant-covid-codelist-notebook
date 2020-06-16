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

# The following medicines are considered Disease Modifying Anti-Rheumatic Drugs or "DMARDs": Azathioprine, Mercaptopurine, Sulfasalazine,
# Hydroxychloroquine, Ciclosporin, Penicillamine, Leflunomide and Mycophenolate mofetil. They are prescribed in primary care however there is likely to be variation in the "shared care aggrements" between GPs and specialists around England. Some patients obtain it from the hospital while others will get it from their GP, you can see the [variation on OpenPrescribing here](https://openprescribing.net/analyse/#org=stp&numIds=0802010G0,0105010E0,0802020G0,0801030L0,1001030F0,1001030L0,0802010M0&denom=total_list_size&selectedTab=map).

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (  
  SELECT bnf_code FROM hscic.presentation WHERE 
  (bnf_code LIKE '0802010G0%'     OR #bnf azathioprine
  bnf_code LIKE '0105010E0%'      OR #bnf sulfasalazine
  bnf_code LIKE '0802020G0%'      OR #bnf ciclosporin   
  bnf_code LIKE '0801030L0%'      OR #bnf mercaptopurine
  bnf_code LIKE '1001030F0%'      OR #bnf penicillamine
  bnf_code LIKE '1001030L0%'      OR #bnf leflunomide
  bnf_code LIKE '1001030J0%'      OR #bnf gold
  bnf_code LIKE '1001030U0%'      OR #bnf methotrexate - mostly oral
  bnf_code LIKE '0801030P0%'      OR #bnf methotrexate - injections, prefilled syringes
  bnf_code LIKE '0802010M0%'         #bnf mycophenolate mofetil - mmf
) 
   )
SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
obj_type IN ('vmp', 'amp')
ORDER BY obj_type, bnf_code, snomed_id '''

dmards_primary_care_meds = bq.cached_read(sql, csv_path=os.path.join('..','data','dmards_primary_care_meds.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
dmards_primary_care_meds
# -


