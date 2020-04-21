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
immuno_meds.count()
# + [markdown]
# ## Dm+d Additions
# Now some of the medicines dn't appear in prescribing data as they are generally hospital only medicines. WE need to include them in case a GP has recorded on a TPP system or we get access to another database. We will manually select these from a list used in a previous study by LSHTM.
#
#


# +
sql = '''
WITH dmd_codes AS (  
  SELECT id FROM dmd.vmp WHERE
  LOWER(nm) LIKE 'afliber%'     OR
  LOWER(nm) LIKE 'canaki%'      OR
  LOWER(nm) LIKE 'avelumab%'    OR
  LOWER(nm) LIKE 'basilix%'     OR
  LOWER(nm) LIKE 'belatac%'     OR
  LOWER(nm) LIKE 'idelalis%'    OR
  LOWER(nm) LIKE 'ipilim%'      OR
  LOWER(nm) LIKE 'nivolum%'     OR
  LOWER(nm) LIKE 'obinutu%'     OR
  LOWER(nm) LIKE 'ofatum%'      OR
  LOWER(nm) LIKE 'panitum%'     OR
  LOWER(nm) LIKE 'pemboliz%'    OR
  LOWER(nm) LIKE 'secukin%'     OR
  LOWER(nm) LIKE 'temsirol%'    OR
  LOWER(nm) LIKE 'tofacit%'     OR
  LOWER(nm) LIKE 'trastuz%'     OR
  LOWER(nm) LIKE 'usteki%'      OR
  LOWER(nm) LIKE 'bendamu%'     OR
  LOWER(nm) LIKE 'carbopla%'    OR
  LOWER(nm) LIKE 'carmust%'     OR
  LOWER(nm) LIKE 'chlormethine%'OR
  LOWER(nm) LIKE 'dacarbaz%'    OR
  LOWER(nm) LIKE 'daunor%'      OR
  LOWER(nm) LIKE 'docetax%'     OR
  LOWER(nm) LIKE 'doxorubi%'    OR
  LOWER(nm) LIKE 'eribuli%'     OR
  LOWER(nm) LIKE 'fludrabi%'    OR
  LOWER(nm) LIKE 'gemcitab%'    OR
  LOWER(nm) LIKE 'idarubi%'     OR
  LOWER(nm) LIKE 'ifosamid%'    OR
  LOWER(nm) LIKE 'irinoteca%'   OR
  LOWER(nm) LIKE 'lomustine%'   OR
  LOWER(nm) LIKE 'plicamy%'     OR
  LOWER(nm) LIKE 'mitobron%'    OR
  LOWER(nm) LIKE 'mitotane%'    OR
  LOWER(nm) LIKE 'oxalip%'      OR
  LOWER(nm) LIKE 'paclit%'      OR
  LOWER(nm) LIKE 'pemetrex%'    OR
  LOWER(nm) LIKE 'ralitrexr%'   OR
  LOWER(nm) LIKE 'razoxane%'    OR
  LOWER(nm) LIKE 'tegafur%'     OR
  LOWER(nm) LIKE 'thiotepa%'    OR
  LOWER(nm) LIKE 'topotecan%'   OR
  LOWER(nm) LIKE 'vinblastine%' OR
  LOWER(nm) LIKE 'vinorebine%'  OR
  LOWER(nm) LIKE 'vismodegib%' 

  ##immunogobulins
  )      
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE id IN (SELECT * FROM dmd_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE vmp IN (SELECT * FROM dmd_codes)

ORDER BY type, nm '''

dmd_immuno_meds = bq.cached_read(sql, csv_path=os.path.join('..','data','dmd_immuno_meds .csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
dmd_immuno_meds.count()
# -

#join the two datframes
immunosuppressants = pd.concat([immuno_meds, dmd_immuno_meds])
immunosuppressants.count()

immunosuppressants.sort_values(["type", "nm"])

immunosuppressants.to_csv(os.path.join('..','data','immunosuppressants_codelist.csv')) #export to csv here

