# https://www.fincen.gov/news-room/enforcement-actions

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

#base_url = "https://www.fincen.gov/news-room/enforcement-actions"
#response = requests.get(base_url)
#soup = BeautifulSoup(response.content, 'html.parser')
#print(soup.prettify())

# Find the table
#table = soup.find('table', {'class': 'table table-hover table-striped'})
#print(table)

from bs4 import BeautifulSoup

# Assuming the HTML content is stored in a variable `html_content`
html_content = '''
<table class="table table-hover table-striped">
        <thead>
    <tr>
                                      <th id="view-title-table-column" class="views-field views-field-title" scope="col">Enforcement Action</th>
                                      <th id="view-field-date-release-table-column" aria-sort="descending" class="views-field views-field-field-date-release is-active" scope="col"><a href="?field_date_release_value=&amp;field_date_release_value_1=&amp;field_tags_financial_institution_target_id=All&amp;order=field_date_release&amp;sort=asc" title="sort by Date">Date<span class="icon glyphicon glyphicon-chevron-down icon-after" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="Sort ascending"></span>
</a></th>
                                      <th id="view-field-matter-no-table-column" class="views-field views-field-field-matter-no" scope="col">Matter Number</th>
                                      <th id="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution" scope="col">Financial Institution</th>
          </tr>
    </thead>
    <tbody>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2024-10-10/FinCEN-TD-Bank-Consent-Order-508FINAL.pdf">In the Matter of TD Bank, N.A. and TD Bank USA, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2024-10-10T12:00:00Z">10/10/2024</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2024-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2024-01-31/FinCEN_Consent_Order_2024-01_FINAL508.pdf">In the Matter of Gyanendra Kumar Asre</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2024-01-31T12:00:00Z">01/31/2024</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2024-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions, Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-11-21/FinCEN_Consent_Order_2023-04_FINAL508.pdf">In the Matter of Binance Holdings Limited, et. al. d/b/a Binance and Binance.com</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2023-11-21T12:00:00Z">11/21/2023</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2023-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-09-29/SHBA_9-28_FINAL_508.pdf">In the Matter of Shinhan Bank America</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2023-09-29T12:00:00Z">09/29/2023</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2023-03	        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-09-15/Bancredito_Consent_FINAL_091523_508C.pdf">In the Matter of Bancrédito International Bank and Trust Corporation</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2023-09-15T12:00:00Z">09/15/2023</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2023-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-27/FinCEN_KTC_ConsentOrder_FINAL_042523.pdf">In the Matter of The Kingdom Trust Company</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2023-04-26T12:00:00Z">04/26/2023</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2023-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-04/Bittrex_Consent_Order_10.11.2022.pdf">In the Matter of Bittrex, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2022-10-11T12:00:00Z">10/11/2022</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2022-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/AS_World_Trading_Consent_Order_FINAL.pdf">In the Matter of A&amp;S World Trading Incorporated</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2022-03-31T12:00:00Z">03/31/2022</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2022-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/USAA_Consent_Order_Final_508_2.pdf">In the Matter of USAA Federal Savings Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2022-03-17T12:00:00Z">03/17/2022</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2022-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/CBOT_Enf_Action_121621_508_FINAL.pdf">In the Matter of CommunityBank of Texas, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2021-12-16T12:00:00Z">12/16/2021</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2021-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2021-08-10/Assessment_BITMEX_508_FINAL_0.pdf">In the Matter of HDR Global Trading Limited, 100x Holdings Limited, ABS Global Trading Limited, Shine Effort Inc. Limited, HDR Global Services (Bermuda) Limited, d/b/a BITMEX</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2021-08-10T12:00:00Z">08/10/2021</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2021-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Assessment_CONA_508_0.pdf">In the Matter of Capital One, National Association</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2021-01-15T12:00:00Z">01/15/2021</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2021-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/HarmonHelix_Assessment_and_SoF_508_101920.pdf">In the Matter of Larry Dean Harmon d/b/a Helix</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2020-10-19T12:00:00Z">10/19/2020</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2020-2        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Michael_LaFontaine_Assessment_02.26.20_508.pdf">In the Matter of Michael LaFontaine</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2020-03-04T12:00:00Z">03/04/2020</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2020-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Assessment_Eric_Powers_Final_for_Posting_04.18.19.pdf">In the Matter of Eric Powers</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2019-04-18T12:00:00Z">04/18/2019</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2019-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/UBS_Assessment_12.17.2018_FINAL_508_Revised_0.pdf">In the Matter of UBS Financial Services Inc.	</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2018-12-17T12:00:00Z">12/17/2018</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2018-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Securities and Futures        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/AJC_Assessment_05.03.18.pdf">In the Matter of Artichoke Joe’s, a California Corporation d/b/a Artichoke Joe’s Casino</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2018-05-03T12:00:00Z">05/03/2018</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2018-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/FinCEN_U.S_Bank_Assesment_FinCEN_review_2.14.18_Final.pdf">In the Matter of U.S. Bank National Association</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2018-02-15T12:00:00Z">02/15/2018</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2018-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/AJC_Proposed_Assessment_Signed_11.15.17.pdf">In the Matter of Artichoke Joe&#039;s Casino [UPDATED, See #2018-02]</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2017-11-17T12:00:00Z">11/17/2017</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2017-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Lone_Star.ASSESSMENT_OF_CIVIL_MONEY_PENALTY_Final_11.01_0.pdf">In the Matter of Lone Star National Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2017-11-01T12:00:00Z">11/01/2017</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2017-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Assessment_for_BTCeVinnik_FINAL2.pdf">In the Matter of BTC-E a/k/a Canton Business Corporation and Alexander Vinnik</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2017-07-27T12:00:00Z">07/27/2017</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2017-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Merchants_Bank_of_California_Assessment_of_CMP_02.24.2017.v2.pdf">In the Matter of Merchants Bank of California, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2017-02-27T12:00:00Z">02/27/2017</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2017-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/WUFSI_Assessment_of_Civil_Money_Penalty_1_19_2017.pdf">In the Matter of Western Union Financial Services, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2017-01-19T12:00:00Z">01/19/2017</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2017-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Bethex_Assessment_Final_0.pdf">In the Matter of Bethex Federal Credit Union </a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2016-12-15T12:00:00Z">12/15/2016</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2016-06        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/20161003_Cantor_Assessment_Final.pdf">In the Matter of CG Technology, L.P. f/k/a Cantor G&amp;W (Nevada), L.P. d/b/a Cantor Gaming</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2016-10-03T12:00:00Z">10/03/2016</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2016-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/20160715_HG_Assessment_Final.pdf">In the Matter of Hawaiian Gardens Casino, Inc. d/b/a The Gardens Casino</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2016-07-15T12:00:00Z">07/15/2016</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2016-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Sparks_Nugget_EA.pdf">In the Matter of Sparks Nugget, Inc., d/b/a John Ascuaga’s Nugget</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2016-04-05T12:00:00Z">04/05/2016</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2016-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Thriftway_Assessment.pdf">In the Matter of Kustandy Rayyan D/B/A Thriftway Food Mart</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2016-03-24T12:00:00Z">03/24/2016</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2016-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Gibraltar_%2520Assessment.pdf">In the Matter of Gibraltar Private Bank and Trust Company</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2016-02-25T12:00:00Z">02/25/2016</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2016-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/20151230.pdf">In the Matter of B.A.K. Precious Metals, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-12-30T12:00:00Z">12/30/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-12        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Precious Metals/Jewelry Industry        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/20151217_Oaks_Assessment.pdf">In the Matter of Oaks Card Club  d/b/a Oaks Club</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-12-17T12:00:00Z">12/17/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-11        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Caesars_Palace_ASSESSMENT.pdf">In the Matter of Desert Palace, Inc. d/b/a Caesars Palace</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-09-08T12:00:00Z">09/08/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-10        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/20150626_Assessment.pdf">In the Matter of Lee’s Snack Shop, Inc. and Hong Ki Yi</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-06-26T12:00:00Z">06/26/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-09        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Mingo_Assessment.pdf">In the Matter of Bank of Mingo</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-06-15T12:00:00Z">06/15/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-08        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Tinian_Dynasty_Assessment.pdf">In the Matter of Hong Kong Entertainment (Overseas) Investments, Ltd., d/b/a Tinian Dynasty Hotel &amp; Casino</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-06-03T12:00:00Z">06/03/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-07        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/20150601Assessment.pdf">In the Matter of King Mail &amp; Wireless Inc., and Ali Al Duais</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-06-01T12:00:00Z">06/01/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-06        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/20150505.pdf">In the Matter of Ripple Labs, Inc. XRP Fund II, LLC Attachment A:  Statement of Facts and Violations Attachment B:  Remedial Framework</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-05-05T12:00:00Z">05/05/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Assessment_20150318_Civil_Money_Penalty_for_Aurora_Sunmart.pdf">In the Matter of Aurora Sunmart Inc. and Jamal Awad</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-03-18T12:00:00Z">03/18/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/20150302%2520Assessment%2520of%2520Civil%2520Money%2520Penalty%2520Trump%2520Taj%2520Mahal%2520%2528post-approval%2520by%2520bankruptcy%2520court%2529.pdf">In the Matter of Trump Taj Mahal Casino Resort</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-03-06T12:00:00Z">03/06/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/FNCB_Assessment.pdf">In the Matter of First National Community Bank of Dunmore, Pennsylvania</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-02-27T12:00:00Z">02/27/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Oppenheimer_Assessment_20150126.pdf">In the Matter of Oppenheimer &amp; Co., Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2015-01-27T12:00:00Z">01/27/2015</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2015-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Securities and Futures        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Haider_Assessment.pdf">In the Matter of Thomas E. Haider</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-12-18T12:00:00Z">12/18/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-08        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/NorthDade_Assessment.pdf">In the Matter of North Dade Community Development Federal Credit Union</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-11-25T12:00:00Z">11/25/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-07        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/BPI_Inc_Assessment.pdf">In the Matter of BPI, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-08-28T12:00:00Z">08/28/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-06        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/GeorgeQue_Assessment_20140820.pdf">In the Matter of George Que</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-08-20T12:00:00Z">08/20/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Mian_Assessment_071514.pdf">In the Matter of Mian, Inc. d/b/a Tower Package Store</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-07-15T12:00:00Z">07/15/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/NMCE_Assessment.pdf">In the Matter of New Milenium Cash Exchange, Inc. and Flor Angella Lopez</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-04-23T12:00:00Z">04/23/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/FinalAdamServiceASSESSMENT2-7-14.pdf">In the Matter of Saleh H. Adam dba Adam Service</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-02-07T12:00:00Z">02/07/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/JPMorgan_ASSESSMENT_01072014_0.pdf">In the Matter of JPMorgan Chase Bank, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2014-01-07T12:00:00Z">01/07/2014</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2014-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/SRVB_Assessment_092413.pdf">In the Matter of Saddle River Valley Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2013-09-24T12:00:00Z">09/24/2013</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2013-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/TD_ASSESSMENT_09222013.pdf">In the Matter of TD Bank, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2013-09-23T12:00:00Z">09/23/2013</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2013-1        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/HSBC_ASSESSMENT.pdf">In the Matter of HSBC Bank USA N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2012-12-11T12:00:00Z">12/11/2012</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2012-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/First_Bank_of_Delaware_11-15-2012_Assessment.pdf">In the Matter of First Bank of Delaware</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2012-11-19T12:00:00Z">11/19/2012</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2012-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/ASSESSMENT_without_consent.pdf">In the Matter of Frank E. Mendoza</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-12-15T12:00:00Z">12/15/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-11        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/ASSESSMENT_SarithMeas_Enforcement_matter_number_2011-10.pdf">In the Matter of Sarith Meas</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-12-08T12:00:00Z">12/08/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-10        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/MohamedSheikhASSESSMENT.pdf">In the Matter of Mohamed Mohamed-Abas Sheikh</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-09-23T12:00:00Z">09/23/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-9        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Altima_Assessment.pdf">In the Matter of Altima, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-09-07T12:00:00Z">09/07/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-8        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/08222011_OceanBank_ASSESSMENT.pdf">In the Matter of Ocean Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-08-22T12:00:00Z">08/22/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-7        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/jackpotjunction.pdf">In the Matter of the Lower Sioux Indian Community d/b/a Jackpot Junction Casino Hotel</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-04-21T12:00:00Z">04/21/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-06        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/PacificNationalBankASSESSMENT.pdf">In the Matter of Pacific National Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-03-24T12:00:00Z">03/24/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-5        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/03-07-2011KaganovASSESSMENT.pdf">In the Matter of Victor Kaganov</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-03-11T12:00:00Z">03/11/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-2        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/11_03_02-13001299070846canned.pdf">In the Matter of Mohamed Abukar Sufi d/b/a Halal Depot</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-03-02T12:00:00Z">03/02/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/11_03_02-13001299070846canned000.pdf">In the Matter of Omar Abukar Sufi d/b/a Halal Depot</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-03-02T12:00:00Z">03/02/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/ZionsAssessment.pdf">In the Matter of Zions First National Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2011-02-11T12:00:00Z">02/11/2011</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2011-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/BalticAssessment.pdf">In the Matter of Baltic Financial Services, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2010-12-16T12:00:00Z">12/16/2010</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2010-5        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2023-04-05/Final_Pinnacle_Assessment_for_FinCEN_Internet_with_Date_and_No_Signature.pdf">In the Matter of Pinnacle Capital Markets, LLC</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2010-09-01T12:00:00Z">09/01/2010</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2010-4        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Securities and Futures        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/PamrapoAssessment.pdf">In the Matter of Pamrapo Savings Bank, S.L.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2010-06-03T12:00:00Z">06/03/2010</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2010-3        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/AssessmentEurobank.pdf">In the Matter of Eurobank, San Juan, Puerto Rico</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2010-05-04T12:00:00Z">05/04/2010</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2010-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/100316095447.pdf">In the Matter of Wachovia Bank, National Association, Charlotte, North Carolina</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2010-03-17T12:00:00Z">03/17/2010</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2010-1        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/2020-05-21/Doha.pdf">In the Matter of Doha Bank, New York Branch</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2009-04-20T12:00:00Z">04/20/2009</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2009-1        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/UBAAssessment.pdf">In the Matter of NY Branch United Bank for Africa</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2008-04-28T12:00:00Z">04/28/2008</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2008-3        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/ElNoaNoa.pdf">In the Matter of El Noa Noa Corporation</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2008-04-14T12:00:00Z">04/14/2008</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2008-2        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/sigue_assement_final.pdf">In the Matter of Sigue Corporation and Sigue, LLC</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2008-01-28T12:00:00Z">01/28/2008</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2008-1        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/ASSESSMENT_In_the_Matter_of_Union_Bank_of_California.pdf">In the Matter of Union Bank of California, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2007-09-17T12:00:00Z">09/17/2007</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2007-2        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/fincen_amex.pdf">In the Matter of American Express Bank International and American Express Travel Related Services Company, Inc</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2007-08-06T12:00:00Z">08/06/2007</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2007-1        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions, Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/beachbank.pdf">In the Matter of Beach Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-12-27T12:00:00Z">12/27/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-09        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/foster.pdf">In the Matter of The Foster Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-12-14T12:00:00Z">12/14/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-08        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/fincen_assessment_of_civil_money_penalty.pdf">In the Matter of Israel Discount Bank of New York</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-10-31T12:00:00Z">10/31/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-07        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/deprez_assessment_07202006.pdf">In the Matter of Deprez’s Quality Jewelry and Loans, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-07-20T12:00:00Z">07/20/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-06        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/liberty_assessment.pdf">In the Matter of Liberty Bank of New York</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-05-19T12:00:00Z">05/19/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/frosty_cmp_consent.pdf">In the Matter of Frosty Food Mart</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-05-09T12:00:00Z">05/09/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/bankatlantic_assessment.pdf">In the Matter of BankAtlantic</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-04-26T12:00:00Z">04/26/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/metro_assessment.pdf">In the Matter of the New York Branch of Metropolitan Bank &amp; Trust Company</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-04-19T12:00:00Z">04/19/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/tonkawa.pdf">In the Matter of the Tonkawa Tribe of Oklahoma and Edward E. Street</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2006-03-24T12:00:00Z">03/24/2006</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2006-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/oppenheimerassessment.pdf">In the Matter of Oppenheimer &amp; Company, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2005-12-29T12:00:00Z">12/29/2005</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2005-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Securities and Futures        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/abn_assessment.pdf">In the Matter of The New York Branch of ABN AMRO Bank N.V</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2005-12-19T12:00:00Z">12/19/2005</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2005-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/bancodechile.pdf">In the Matter of Banco de Chile-New York and Banco de Chile-Miami</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2005-10-12T12:00:00Z">10/12/2005</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2005-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/arab081705.pdf">In the Matter of The New York Branch of Arab Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2005-08-17T12:00:00Z">08/17/2005</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2005-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/gulf070505.pdf">In the Matter of Gulf Corporation</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2005-07-05T12:00:00Z">07/05/2005</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2005-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/amsouthassessmentcivilmoney.pdf">In the Matter of AmSouth Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2004-10-12T12:00:00Z">10/12/2004</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2004-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/riggsassessment3.pdf">In the Matter of Riggs Bank, NA</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2004-05-13T12:00:00Z">05/13/2004</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2004-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/hartsfieldassessment.pdf">In the Matter of Hartsfield Capital Securities, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2003-11-24T12:00:00Z">11/24/2003</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2003-05        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Securities and Futures        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/koreaexchangeassessment.pdf">In the Matter of Korea Exchange Bank, New York, New York</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2003-06-24T12:00:00Z">06/24/2003</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2003-04        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/greenvilleassessfinal.pdf">In the Matter of Greenville Riverboat, LLC d/b/a Lighthouse Point Casino</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2003-05-23T12:00:00Z">05/23/2003</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2003-03        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/western_union_assessment.pdf">In the Matter of Western Union Financial Services, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2003-03-06T12:00:00Z">03/06/2003</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2003-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/bancopopular.pdf">In the Matter of Banco Popular de Puerto Rico</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2003-01-16T12:00:00Z">01/16/2003</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2003-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/geassessfinal.pdf">In the Matter of Great Eastern Bank of Florida</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2002-09-04T12:00:00Z">09/04/2002</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2002-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/sovereignbank.pdf">In the Matter of Sovereign Bank</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2002-04-08T12:00:00Z">04/08/2002</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2002-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Depository Institutions        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/plett.pdf">In the Matter of Angelina Plett</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2001-09-04T12:00:00Z">09/04/2001</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2001-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/sivigliano.pdf">In the Matter of Joseph A. Sivigliano</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2001-09-04T12:00:00Z">09/04/2001</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2001-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/rainbowcasinovicksburg.pdf">In the Matter of Rainbow Casino Vicksburg</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-12-20T12:00:00Z">12/20/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2000-02        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Casinos        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/casadecambiorega.pdf">In the Matter of Casa De Cambio Rega</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-10-23T12:00:00Z">10/23/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">2000-01        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/checkcashing.pdf">In the Matter of D &amp; S Check Cashing, Inc. and Michael Rose</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-06-29T12:00:00Z">06/29/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">MSB99-012        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/msb99009.pdf">In the Matter of Mex Pesos Currency Exchange</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-04-19T12:00:00Z">04/19/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">MSB99-009        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">Money Services Businesses        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/ameristar.pdf">In the Matter of Ameristar Casino Vicksburg, Inc.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-03-06T12:00:00Z">03/06/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-003        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/polishslavic.pdf">In the Matter of Polish &amp; Slavic Federal Credit Union</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-01-18T12:00:00Z">01/18/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">DI 99-011        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/sunflowerbank.pdf">In the Matter of Sunflower Bank, N.A.</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="2000-01-06T12:00:00Z">01/06/2000</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">DI 99-008        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/islecaprivicksburg.pdf">In the Matter of Riverboat Corporation of Mississippi-Vicksburg, d/b/a Isle of Capri-Vicksburg</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="1999-09-30T12:00:00Z">09/30/1999</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-005        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/grandcasinosmiss.pdf">In the Matter of Grand Casinos of Mississippi, Inc. Biloxi</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="1999-09-30T12:00:00Z">09/30/1999</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-007        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/islecapribiloxi.pdf">In the Matter of Riverboat Corporation of Mississippi, d/b/a Isle of Capri Casino-Biloxi</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="1999-09-30T12:00:00Z">09/30/1999</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-004        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/ladyluck.pdf">In the Matter of Lady Luck Mississippi, Inc., d/b/a Lady Luck Natchez</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="1999-08-09T12:00:00Z">08/09/1999</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-006        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/casinomagic.pdf">In the Matter of Biloxi Casino Corp., d/b/a/ Casino Magic-Biloxi</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="1999-08-03T12:00:00Z">08/03/1999</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-002        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
      <tr>
                                                                      <td headers="view-title-table-column" class="views-field views-field-title"><a href="https://www.fincen.gov/sites/default/files/enforcement_action/gulfsidecasino.pdf">In the Matter of Gulfside Casino Partnership, d/b/a Copa Casino</a>        </td>
                                                                      <td headers="view-field-date-release-table-column" class="views-field views-field-field-date-release is-active"><time datetime="1999-04-23T12:00:00Z">04/23/1999</time>
        </td>
                                                                      <td headers="view-field-matter-no-table-column" class="views-field views-field-field-matter-no">CAS-99-001        </td>
                                                                      <td headers="view-field-tags-financial-institution-table-column" class="views-field views-field-field-tags-financial-institution">        </td>
          </tr>
    </tbody>
</table>
'''

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table body (ignores headers)
table_body = soup.find('tbody')

# Extract the links from the rows
links = []
for tr in table_body.find_all('tr'):
    link = tr.find('a')
    if link:
        links.append(link['href'])

# Download the files
for link in links:
    filename = link.split('/')[-1]
    response = requests.get(link)
    print(f"Downloading {filename}.pdf")
    with open(f"data/enforcement_actions/documents/fincen/{filename}.pdf", 'wb') as f:
        f.write(response.content)
