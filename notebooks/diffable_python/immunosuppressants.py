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

# This is list of immunosuppressants medicines. It will need to be combined with [work on steroids](https://github.com/ebmdatalab/steroids-covid-codelist-notebook/tree/master/notebooks) for a compete definitions

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (  
  SELECT bnf_code FROM hscic.presentation WHERE 
  (bnf_code LIKE '0801%'      OR #bnf sect cytotoxic drugs - NHSD did not include?
  bnf_code LIKE '0802%'      OR #bnf sect drugs affecting immune response
  bnf_code LIKE '100103%'       #bnf - sect rhuematic disease suppressant drugs
) 
  AND
  (bnf_code NOT LIKE '0802020T0%XAX'  #BNF tacrolimus mouthwash
)
   )
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, nm '''

immuno_meds = bq.cached_read(sql, csv_path=os.path.join('..','data','immuno_meds .csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
immuno_meds
# + [markdown]
# Needed to be extracted from dm+d
# aflibercept
# alemtuzumab see discrepancy files held locally
#
#
# -


#
