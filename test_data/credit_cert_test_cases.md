{
  "document_title": "信用证智能审单系统测试数据集（含OCR原始文本）",
  "version": "2.1",
  "description": "基于UCP600和ISBP745标准的10组信用证审单测试数据，包含结构化字段与OCR原始文本双版本，用于阶段A规则校验与阶段B OCR识别测试",
  "total_cases": 10,
  "cases": [
    {
      "case_id": "case_01",
      "case_description": "完全相符案例 - 无不符点（农产品：巴西大豆）",
      "letter_of_credit": {
        "lc_number": "LC2024-BZ-001",
        "issuing_bank": "中国农业银行深圳分行",
        "advising_bank": "桑坦德银行圣保罗分行",
        "applicant": {
          "name": "深圳绿源饲料集团有限公司",
          "address": "深圳市南山区科技南路88号绿源大厦"
        },
        "beneficiary": {
          "name": "Agroexport Brasil S.A.",
          "address": "Avenida Paulista 1000, São Paulo, SP 01310-000, Brazil"
        },
        "currency": "USD",
        "amount": 485000.00,
        "amount_tolerance": "+/- 5%",
        "goods_description": "5000 Metric Tons of Brazilian Non-GMO Yellow Soybeans, Crop 2024, Protein Min 35%, packed in bulk",
        "latest_shipment_date": "2024-08-15",
        "expiry_date": "2024-09-05",
        "expiry_place": "Santos, Brazil",
        "presentation_period": "21 days after the date of shipment but within the validity of this credit",
        "loading_port": "Santos, Brazil",
        "discharge_port": "Shenzhen, China",
        "trade_terms": "CIF Shenzhen",
        "partial_shipment": "Allowed",
        "transhipment": "Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals and 2 copies",
          "Full set of clean on board ocean bills of lading made out to order and blank endorsed, marked freight prepaid, notify applicant",
          "Insurance policy or certificate for 110% of CIF value covering All Risks and War Risks",
          "Quality Certificate issued by SGS",
          "Weight Certificate issued by CIQ"
        ],
        "additional_conditions": [
          "All documents must show L/C number",
          "Shipment to be effected by regular line vessels"
        ],
        "raw_text": "MESSAGE TYPE: MT700\nISSUE OF DOCUMENTARY CREDIT\nSENDER: ABOCCNBJ410\nRECEIVER: BSCHBRSPXXXX\n-----------------------------\nFORM OF DOC.CREDIT: IRREVOCABLE\nDOC.CREDIT NUMBER: LC2024-BZ-001\nDATE OF ISSUE: 20240715\nEXPIRY DATE: 20240905\nPLACE OF EXPIRY: SANTOS,BRAZIL\nAPPLICANT:\nSHENZHEN LVYUAN FEED GROUP CO.,LTD.\nNO.88 KEJI SOUTH ROAD, NANSHAN DIST\nSHENZHEN, CHINA\nBENEFICIARY:\nAGROEXPORT BRASIL S.A.\nAVENIDA PAULISTA 1000\nSAO PAULO, SP 01310-000\nBRAZIL\nAMOUNT: USD485,000.00\n(U.S.DOLLARS FOUR HUNDRED EIGHTY-FIVE THOUSAND ONLY)\n+/- 5 PCT TOLERANCE ALLOWED\nAVAILABLE WITH/BY: ANY BANK\nBY NEGOTIATION\nDRAFTS AT...: SIGHT\nDRAWEE: ABOCCNBJ410\nPARTIAL SHIPMENTS: ALLOWED\nTRANSSHIPMENT: ALLOWED\nLOADING IN CHARGE: SANTOS, BRAZIL\nFOR TRANSPORT TO: SHENZHEN, CHINA\nLATEST DATE OF SHIPMENT: 20240815\nDESCRIPTION OF GOODS:\n5000 METRIC TONS OF BRAZILIAN NON-GMO\nYELLOW SOYBEANS, CROP 2024, PROTEIN MIN 35%\nPACKED IN BULK\nPRICE TERMS: CIF SHENZHEN\nDOCUMENTS REQUIRED:\n+SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS AND 2 COPIES\n+FULL SET CLEAN ON BOARD OCEAN BILLS OF LADING\nMADE OUT TO ORDER AND BLANK ENDORSED\nMARKED FREIGHT PREPAID NOTIFY APPLICANT\n+INSURANCE POLICY/CERTIFICATE FOR 110PCT OF CIF\nVALUE COVERING ALL RISKS AND WAR RISKS\n+QUALITY CERTIFICATE ISSUED BY SGS\n+WEIGHT CERTIFICATE ISSUED BY CIQ\nPERIOD FOR PRESENTATION: 21 DAYS AFTER SHIPMENT\nBUT WITHIN CREDIT VALIDITY\nCONFIRMATION INSTRUCTIONS: WITHOUT\nREIMBURSING BANK: ABOCCNBJ410\nINSTRUCTIONS TO NEGOTIATING BANK:\nUPON RECEIPT OF COMPLYING DOCUMENTS, WE SHALL\nREIMBURSE YOU AS PER YOUR INSTRUCTIONS\nTHIS CREDIT IS SUBJECT TO UCP600 (2007 REVISION)"
      },
      "commercial_invoice": {
        "invoice_number": "AGX-2024-0812",
        "invoice_date": "2024-08-10",
        "issued_by": "Agroexport Brasil S.A.",
        "issued_to": "深圳绿源饲料集团有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "Brazilian Non-GMO Yellow Soybeans, Crop 2024, Protein Min 35%, packed in bulk",
            "quantity": 5000,
            "unit": "Metric Tons",
            "unit_price": 97.00,
            "amount": 485000.00
          }
        ],
        "total_amount": 485000.00,
        "trade_terms": "CIF Shenzhen",
        "raw_text": "COMMERCIAL INVOICE\n\nINVOICE NO.: AGX-2024-0812\nDATE: AUGUST 10, 2024\nL/C NO.: LC2024-BZ-001\n\nSELLER/EXPORTER:\nAGROEXPORT BRASIL S.A.\nAVENIDA PAULISTA 1000\nSAO PAULO, SP 01310-000\nBRAZIL\nTEL: +55-11-3456-7890\n\nBUYER/IMPORTER:\nSHENZHEN LVYUAN FEED GROUP CO.,LTD.\nNO.88 KEJI SOUTH ROAD, NANSHAN DISTRICT\nSHENZHEN 518057, CHINA\n\nPORT OF LOADING: SANTOS, BRAZIL\nPORT OF DISCHARGE: SHENZHEN, CHINA\nTERMS OF DELIVERY: CIF SHENZHEN\n\n------------------------------------------------\nDESCRIPTION                      QTY      U.PRICE   AMOUNT\n------------------------------------------------\nBRAZILIAN NON-GMO YELLOW         5,000    USD97.00  USD485,000.00\nSOYBEANS, CROP 2024             MT\nPROTEIN MIN 35%\nPACKED IN BULK\n------------------------------------------------\nTOTAL:                           5,000 MT         USD485,000.00\n\nSAY TOTAL: U.S.DOLLARS FOUR HUNDRED EIGHTY-FIVE THOUSAND ONLY\n\nBANK DETAILS:\nBENEFICIARY: AGROEXPORT BRASIL S.A.\nBANK: BANCO SANTANDER BRASIL S.A.\nACCOUNT NO.: 123456789-0\nSWIFT: BSCHBRSP\n\nWe certify that the goods are of Brazilian origin\n\nAuthorized Signature: _______________\nFor and on behalf of\nAgroexport Brasil S.A."
      },
      "bill_of_lading": {
        "bl_number": "MSC-SNT-2024-4451",
        "shipper": "Agroexport Brasil S.A., Avenida Paulista 1000, São Paulo, Brazil",
        "consignee": "To Order",
        "notify_party": "深圳绿源饲料集团有限公司, 深圳市南山区科技南路88号绿源大厦",
        "vessel": "MSC Geneva",
        "voyage": "V.248W",
        "port_of_loading": "Santos, Brazil",
        "port_of_discharge": "Shenzhen, China",
        "onboard_date": "2024-08-12",
        "issue_date": "2024-08-13",
        "goods_description": "5000 Metric Tons of Brazilian Non-GMO Yellow Soybeans, Crop 2024, Protein Min 35%, packed in bulk",
        "number_of_packages": "In Bulk",
        "gross_weight": "5000 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "MSC Mediterranean Shipping Company, Santos Agent",
        "raw_text": "BILL OF LADING\n\nB/L NO.: MSC-SNT-2024-4451\nBOOKING NO.: BK20240812001\n\nSHIPPER:\nAGROEXPORT BRASIL S.A.\nAVENIDA PAULISTA 1000\nSAO PAULO, SP 01310-000\nBRAZIL\nTEL: +55-11-3456-7890\n\nCONSIGNEE:\nTO ORDER\n\nNOTIFY PARTY:\nSHENZHEN LVYUAN FEED GROUP CO.,LTD.\nNO.88 KEJI SOUTH ROAD, NANSHAN DIST\nSHENZHEN 518057, CHINA\nTEL: +86-755-1234-5678\n\nVESSEL: MSC GENEVA\nVOYAGE NO.: V.248W\nFLAG: PANAMA\n\nPORT OF LOADING: SANTOS, BRAZIL\nPORT OF DISCHARGE: SHENZHEN, CHINA\nPLACE OF RECEIPT: SANTOS, BRAZIL\nPLACE OF DELIVERY: SHENZHEN, CHINA\n\nCONTAINER NO.: N/A (BULK CARGO)\n\nDESCRIPTION OF PACKAGES AND GOODS:\n5,000 METRIC TONS OF BRAZILIAN NON-GMO\nYELLOW SOYBEANS, CROP 2024, PROTEIN MIN 35%\nPACKED IN BULK\n\nGROSS WEIGHT: 5,000.000 METRIC TONS\nMEASUREMENT: N/A\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINAL B(s)/L: THREE(3)\n\nPLACE AND DATE OF ISSUE: SANTOS, AUGUST 13, 2024\n\nLOADED ON BOARD THE VESSEL\nDATE: AUGUST 12, 2024\n\nBY:\n_________________________________\nMSC MEDITERRANEAN SHIPPING COMPANY\nSANTOS AGENT\n\nLADEN ON BOARD THE VESSEL IN APPARENT\nGOOD ORDER AND CONDITION UNLESS OTHERWISE\nNOTED (CLEAN ON BOARD)\n\nFREIGHT PAYABLE AT: DESTINATION"
      },
      "insurance_policy": {
        "policy_number": "PICC-SH-2024-089234",
        "insured": "Agroexport Brasil S.A.",
        "insurance_amount": 533500.00,
        "currency": "USD",
        "coverage": "All Risks and War Risks",
        "goods_description": "5000 Metric Tons of Brazilian Non-GMO Yellow Soybeans",
        "vessel": "MSC Geneva",
        "from": "Santos, Brazil",
        "to": "Shenzhen, China",
        "issue_date": "2024-08-11",
        "claims_payable_at": "Shenzhen, China",
        "raw_text": "THE PEOPLE'S INSURANCE COMPANY OF CHINA\nSHANGHAI BRANCH\n\nMARINE CARGO INSURANCE POLICY\n\nPOLICY NO.: PICC-SH-2024-089234\n\nINSURED: AGROEXPORT BRASIL S.A.\nAVENIDA PAULISTA 1000, SAO PAULO, BRAZIL\n\nL/C NO.: LC2024-BZ-001\n\nThis Policy of Insurance witnesses that The People's Insurance Company of China (hereinafter called \"The Company\"), at the request of the Insured named in the Schedule hereto, and in consideration of the agreed premium paid to the Company by the Insured, undertakes to insure the undermentioned goods in transportation subject to the conditions of this Policy as per the Clauses printed below and other special clauses attached hereto.\n\n-------------------------------------------\nMARKS & NOS.  QUANTITY    DESCRIPTION OF GOODS\n-------------------------------------------\nN/M          5,000 MT    BRAZILIAN NON-GMO YELLOW\n                         SOYBEANS, CROP 2024\n\nAMOUNT INSURED: USD533,500.00\n(U.S.DOLLARS FIVE HUNDRED THIRTY-THREE THOUSAND FIVE HUNDRED ONLY)\n\nPREMIUM: AS ARRANGED\nDATE OF COMMENCEMENT: AUGUST 11, 2024\nPER CONVEYANCE: S.S. MSC GENEVA V.248W\nFROM: SANTOS, BRAZIL\nTO: SHENZHEN, CHINA\n\nCONDITIONS:\nCOVERING ALL RISKS AND WAR RISKS\nAS PER CIC OF PICC DATED 01/01/1981\n\nCLAIMS PAYABLE AT: SHENZHEN, CHINA\nIN THE CURRENCY OF: USD\n\nDATE: AUGUST 11, 2024\nPLACE: SHANGHAI, CHINA\n\nAuthorized Signature\n_________________________\nFor and on behalf of\nTHE PEOPLE'S INSURANCE CO. OF CHINA\nSHANGHAI BRANCH\n\nTHIS POLICY IS ISSUED IN 2 ORIGINALS"
      },
      "presentation_date": "2024-08-28",
      "expected_result": {
        "has_discrepancies": false,
        "discrepancies": [],
        "overall_assessment": "所有单据与信用证条款完全相符，建议承付。"
      }
    },
    {
      "case_id": "case_02",
      "case_description": "完全相符案例 - 无不符点（机械设备：德国数控机床）",
      "letter_of_credit": {
        "lc_number": "LC2024-DE-089",
        "issuing_bank": "中国银行青岛分行",
        "advising_bank": "德意志银行法兰克福分行",
        "applicant": {
          "name": "青岛海创重工科技有限公司",
          "address": "青岛市黄岛区香江路126号"
        },
        "beneficiary": {
          "name": "DMG MORI Aktiengesellschaft",
          "address": "Gildemeisterstraße 60, 33689 Bielefeld, Germany"
        },
        "currency": "EUR",
        "amount": 1250000.00,
        "amount_tolerance": "+/- 0%",
        "goods_description": "2 Units CNC Vertical Machining Center Model DMU 85 monoBLOCK, including standard accessories, spare parts for 2 years operation",
        "latest_shipment_date": "2024-10-30",
        "expiry_date": "2024-11-20",
        "expiry_place": "Frankfurt, Germany",
        "presentation_period": "15 days after the date of shipment but within the validity of this credit",
        "loading_port": "Hamburg, Germany",
        "discharge_port": "Qingdao, China",
        "trade_terms": "CIF Qingdao",
        "partial_shipment": "Not Allowed",
        "transhipment": "Not Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 2 originals",
          "Full set of clean on board ocean bills of lading consigned to applicant, marked freight prepaid",
          "Insurance policy for 110% of CIF value covering Institute Cargo Clauses (A) and War Clauses",
          "Packing List in 3 originals",
          "Certificate of Origin issued by Chamber of Industry and Commerce"
        ],
        "additional_conditions": [
          "All documents must be issued in English",
          "Shipping marks: HCKG/QD2024/01-02"
        ],
        "raw_text": "MT700 ISSUE OF DOCUMENTARY CREDIT\nBANK OF CHINA QINGDAO BRANCH\nSWIFT: BKCHCNBJ500\n\nSEQUENCE OF TOTAL: 1/1\nFORM OF DOC.CREDIT: IRREVOCABLE\nDOC.CREDIT NUMBER: LC2024-DE-089\nDATE OF ISSUE: 20240925\nAPPLICABLE RULES: UCP LATEST VERSION\nDATE AND PLACE OF EXPIRY: 20241120 FRANKFURT, GERMANY\nAPPLICANT:\nQINGDAO HAICHUANG HEAVY INDUSTRY TECH CO.,LTD.\nNO.126 XIANGJIANG ROAD, HUANGDAO DISTRICT\nQINGDAO 266555, CHINA\nBENEFICIARY:\nDMG MORI AKTIENGESELLSCHAFT\nGILDEMEISTERSTRASSE 60\n33689 BIELEFELD, GERMANY\nCURRENCY CODE/AMOUNT: EUR1,250,000.00\n(ONE MILLION TWO HUNDRED FIFTY THOUSAND EURO)\nZERO TOLERANCE\nAVAILABLE WITH/BY: DEUTSCHE BANK FRANKFURT\nBY ACCEPTANCE\nDRAFTS AT: 90 DAYS AFTER SIGHT\nDRAWEE: BANK OF CHINA QINGDAO BRANCH\nPARTIAL SHIPMENTS: NOT ALLOWED\nTRANSSHIPMENT: NOT ALLOWED\nLOADING/DISPATCH/TAKING IN CHARGE: HAMBURG, GERMANY\nFOR TRANSPORTATION TO: QINGDAO, CHINA\nLATEST DATE OF SHIPMENT: 20241030\nDESCRIPTION OF GOODS:\n2 UNITS CNC VERTICAL MACHINING CENTER\nMODEL DMU 85 MONOBLOCK\nINCLUDING STANDARD ACCESSORIES\nSPARE PARTS FOR 2 YEARS OPERATION\nPRICE TERMS: CIF QINGDAO\nDOCUMENTS REQUIRED:\n1. SIGNED COMMERCIAL INVOICE IN 2 ORIGINALS\n2. FULL SET CLEAN ON BOARD OCEAN BILLS OF LADING\n   CONSIGNED TO APPLICANT, MARKED FREIGHT PREPAID\n3. INSURANCE POLICY FOR 110% OF CIF VALUE\n   COVERING INSTITUTE CARGO CLAUSES (A) AND WAR CLAUSES\n4. PACKING LIST IN 3 ORIGINALS\n5. CERTIFICATE OF ORIGIN ISSUED BY CHAMBER OF INDUSTRY\n   AND COMMERCE\nADDITIONAL CONDITIONS:\nALL DOCUMENTS MUST BE ISSUED IN ENGLISH\nSHIPPING MARKS: HCKG/QD2024/01-02\nPRESENTATION PERIOD: 15 DAYS AFTER SHIPMENT\nCONFIRMATION: WITHOUT"
      },
      "commercial_invoice": {
        "invoice_number": "DMG-2024-INV-4451",
        "invoice_date": "2024-10-25",
        "issued_by": "DMG MORI Aktiengesellschaft",
        "issued_to": "青岛海创重工科技有限公司",
        "currency": "EUR",
        "goods": [
          {
            "description": "2 Units CNC Vertical Machining Center Model DMU 85 monoBLOCK, including standard accessories, spare parts for 2 years operation",
            "quantity": 2,
            "unit": "Units",
            "unit_price": 625000.00,
            "amount": 1250000.00
          }
        ],
        "total_amount": 1250000.00,
        "trade_terms": "CIF Qingdao",
        "raw_text": "DMG MORI\nAKTIENGESELLSCHAFT\n\nCOMMERCIAL INVOICE\n\nInvoice No.: DMG-2024-INV-4451\nDate: October 25, 2024\nCustomer No.: CN-778234\nL/C Ref.: LC2024-DE-089\n\nSold to:\nQINGDAO HAICHUANG HEAVY INDUSTRY TECH CO.,LTD.\nNO.126 XIANGJIANG ROAD\nHUANGDAO DISTRICT, QINGDAO 266555\nCHINA\nVAT NO.: 91370211MA3XXXXXX\n\nShip to:\nSame as above\n\n=========================================================================\nItem  Description                                    Qty    Unit Price    Amount\n=========================================================================\n01    CNC VERTICAL MACHINING CENTER                  2      EUR625,000.00 EUR1,250,000.00\n      MODEL DMU 85 MONOBLOCK                         UNITS\n      SERIAL NO.: DMU85-2024-0891/0892\n      INCLUDING STANDARD ACCESSORIES\n      SPARE PARTS FOR 2 YEARS OPERATION\n      HS CODE: 8457.10.00\n=========================================================================\n                                                    TOTAL:    EUR1,250,000.00\n\nSAY EURO ONE MILLION TWO HUNDRED FIFTY THOUSAND ONLY\n\nTERMS: CIF QINGDAO\nORIGIN: GERMANY\nSHIPPING MARKS: HCKG/QD2024/01-02\nWEIGHT: 18,500 KGS\nDIMENSIONS: 4 WOODEN CASES\n\nBank Details:\nCommerzbank AG Bielefeld\nKonto: 1234567890\nBLZ: 48040035\nIBAN: DE56480400350123456790\nSWIFT: COBADEFFXXX\n\nThis is a computer-generated invoice and requires no signature.\nDMG MORI AG - Registergericht Bielefeld HRB 37519\nGeschäftsführung: Masahiko Mori, Christian Thönes"
      },
      "bill_of_lading": {
        "bl_number": "HLCU-HAM-2024-78234",
        "shipper": "DMG MORI Aktiengesellschaft, Gildemeisterstraße 60, Bielefeld, Germany",
        "consignee": "青岛海创重工科技有限公司",
        "notify_party": "青岛海创重工科技有限公司",
        "vessel": "Hapag-Lloyd Express",
        "voyage": "V.142E",
        "port_of_loading": "Hamburg, Germany",
        "port_of_discharge": "Qingdao, China",
        "onboard_date": "2024-10-28",
        "issue_date": "2024-10-28",
        "goods_description": "2 Units CNC Vertical Machining Center Model DMU 85 monoBLOCK, including standard accessories, spare parts for 2 years operation",
        "number_of_packages": "4 Wooden Cases",
        "gross_weight": "18.5 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "Hapag-Lloyd AG, Hamburg",
        "raw_text": "HAPAG-LLOYD\nBILL OF LADING\n\nB/L NO.: HLCU-HAM-2024-78234\nEXPORT REFERENCES: DMG-2024-INV-4451\n\nSHIPPER/EXPORTER:\nDMG MORI AKTIENGESELLSCHAFT\nGILDEMEISTERSTRASSE 60\n33689 BIELEFELD, GERMANY\nCONTACT: MR. KLAUS SCHMIDT\nTEL: +49-5205-74-0\n\nCONSIGNEE:\nQINGDAO HAICHUANG HEAVY INDUSTRY TECH CO.,LTD.\nNO.126 XIANGJIANG ROAD\nHUANGDAO DISTRICT, QINGDAO 266555\nCHINA\n\nNOTIFY PARTY (COMPLETE NAME AND ADDRESS):\nSAME AS CONSIGNEE\n\nPRE-CARRIAGE BY: TRUCK\nPLACE OF RECEIPT: BIELEFELD, GERMANY\n\nOCEAN VESSEL: HAPAG-LLOYD EXPRESS\nVOYAGE NO.: V.142E\nPORT OF LOADING: HAMBURG, GERMANY\nPORT OF DISCHARGE: QINGDAO, CHINA\nPLACE OF DELIVERY: QINGDAO, CHINA\n\nCONTAINER NO. SEAL NO. MARKS & NOS.   DESCRIPTION OF PACKAGES\n-----------------------------------------------\nHLXU1234567  1234567 HCKG/QD2024/01-02  4 WOODEN CASES\n                                    STC:\n                                    2 UNITS CNC VERTICAL\n                                    MACHINING CENTER MODEL\n                                    DMU 85 MONOBLOCK\n                                    INCLUDING ACCESSORIES\n                                    AND SPARE PARTS\n                                    HS CODE: 8457.10.00\n                                    G.W.: 18,500 KGS\n                                    MEAS.: 85 CBM\n\nTOTAL NUMBER OF PACKAGES: FOUR (4) WOODEN CASES ONLY\n\nFREIGHT & CHARGES: PREPAID\nDECLARED VALUE: N/A\n\nPLACE AND DATE OF ISSUE: HAMBURG, OCTOBER 28, 2024\nNUMBER OF ORIGINAL B(s)/L: THREE (3)\n\nLOADED ON BOARD DATE: OCTOBER 28, 2024\n\nHAPAG-LLOYD AG\nAS CARRIER\nBy: ___________________________\nAuthorized Agent\n\nCLEAN ON BOARD - SHIPPED IN APPARENT GOOD ORDER AND CONDITION\nUNLESS OTHERWISE NOTED IN THIS B/L"
      },
      "insurance_policy": {
        "policy_number": "ALLIANZ-DE-2024-15678",
        "insured": "DMG MORI Aktiengesellschaft",
        "insurance_amount": 1375000.00,
        "currency": "EUR",
        "coverage": "Institute Cargo Clauses (A) and Institute War Clauses",
        "goods_description": "2 Units CNC Vertical Machining Center Model DMU 85 monoBLOCK",
        "vessel": "Hapag-Lloyd Express",
        "from": "Hamburg, Germany",
        "to": "Qingdao, China",
        "issue_date": "2024-10-27",
        "claims_payable_at": "Qingdao, China",
        "raw_text": "ALLIANZ GLOBAL CORPORATE & SPECIALTY SE\nMARINE CARGO INSURANCE CERTIFICATE\n\nCERTIFICATE NO.: ALLIANZ-DE-2024-15678\n\nNAMED INSURED: DMG MORI AKTIENGESELLSCHAFT\nGILDEMEISTERSTRASSE 60\n33689 BIELEFELD, GERMANY\n\nTHIS IS TO CERTIFY THAT insurance has been effected with Allianz Global Corporate & Specialty SE (herein called the Underwriters) under the Open Policy issued to the Named Insured.\n\nVOYAGE: FROM HAMBURG, GERMANY TO QINGDAO, CHINA\nVESSEL: HAPAG-LLOYD EXPRESS V.142E\n\nINSURED VALUE: EUR1,375,000.00\n(ONE MILLION THREE HUNDRED SEVENTY-FIVE THOUSAND EURO)\n\nINTEREST INSURED:\n2 UNITS CNC VERTICAL MACHINING CENTER MODEL DMU 85 MONOBLOCK\nINVOICE VALUE: EUR1,250,000.00\nPLUS 10%\n\nCONDITIONS: INSTITUTE CARGO CLAUSES (A) 1/1/82\n            INSTITUTE WAR CLAUSES (CARGO) 1/1/82\n            INSTITUTE STRIKES CLAUSES (CARGO) 1/1/82\n\nDEDUCTIBLE: NIL\n\nCLAIMS PAYABLE IN: QINGDAO, CHINA\nSETTLING AGENT: ALLIANZ CHINA, QINGDAO BRANCH\n\nDATE OF ISSUE: OCTOBER 27, 2024\nPLACE: HAMBURG, GERMANY\n\nAUTHORIZED SIGNATURE\n\nALLIANZ HAUPTVERTRETUNG BIELEFELD\nTHIS CERTIFICATE IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-11-10",
      "expected_result": {
        "has_discrepancies": false,
        "discrepancies": [],
        "overall_assessment": "所有单据与信用证条款完全相符，建议承付。"
      }
    },
    {
      "case_id": "case_03",
      "case_description": "商业发票不符点案例（化工原料：韩国聚酯切片）",
      "letter_of_credit": {
        "lc_number": "LC2024-KR-156",
        "issuing_bank": "中国建设银行宁波分行",
        "advising_bank": "新韩银行首尔分行",
        "applicant": {
          "name": "宁波恒逸石化有限公司",
          "address": "宁波市镇海区大运路168号"
        },
        "beneficiary": {
          "name": "SK Chemicals Co., Ltd.",
          "address": "26 Jong-ro, Jongno-gu, Seoul 03188, Korea"
        },
        "currency": "USD",
        "amount": 320000.00,
        "amount_tolerance": "+/- 0%",
        "goods_description": "200 Metric Tons of PET Resin Bottle Grade CB-602, Intrinsic Viscosity 0.80±0.02 dL/g, packed in 1100KG jumbo bags",
        "latest_shipment_date": "2024-07-25",
        "expiry_date": "2024-08-15",
        "expiry_place": "Seoul, Korea",
        "presentation_period": "15 days after the date of shipment",
        "loading_port": "Busan, Korea",
        "discharge_port": "Ningbo, China",
        "trade_terms": "CIF Ningbo",
        "partial_shipment": "Not Allowed",
        "transhipment": "Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading made out to order, marked freight prepaid, notify applicant",
          "Insurance policy for 110% of CIF value covering All Risks",
          "Quality Certificate issued by manufacturer"
        ],
        "additional_conditions": [
          "Invoice amount must not exceed L/C amount",
          "All documents to be in English"
        ],
        "raw_text": "MT700 DOCUMENTARY CREDIT\nSEQUENCE: 1/1\nFORM: IRREVOCABLE\nDOC.CREDIT NO.: LC2024-KR-156\nISSUE DATE: 20240701\nEXPIRY: 20240815 SEOUL, KOREA\nAPPLICANT:\nNINGBO HENGYI PETROCHEMICAL CO.,LTD.\nNO.168 DAYUN ROAD, ZHENHAI DISTRICT\nNINGBO 315200, CHINA\nBENEFICIARY:\nSK CHEMICALS CO., LTD.\n26 JONG-RO, JONGNO-GU\nSEOUL 03188, REPUBLIC OF KOREA\nAMOUNT: USD320,000.00 (NO TOLERANCE)\nAVAILABLE: BY NEGOTIATION WITH SHINHAN BANK SEOUL\nDRAFTS: AT SIGHT\nDRAWEE: CCBNINGBO\nPARTIAL SHIPMENT: NOT ALLOWED\nTRANSSHIPMENT: ALLOWED\nLOADING: BUSAN, KOREA\nDESTINATION: NINGBO, CHINA\nLATEST SHIPMENT: 20240725\nGOODS: 200 METRIC TONS PET RESIN BOTTLE GRADE CB-602\nINTRINSIC VISCOSITY 0.80±0.02 DL/G\nPACKED IN 1100KG JUMBO BAGS\nPRICE: CIF NINGBO\nDOCUMENTS:\n-SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n-FULL SET CLEAN ON BOARD B/L TO ORDER\n-FREIGHT PREPAID, NOTIFY APPLICANT\n-INSURANCE POLICY 110% OF CIF COVERING ALL RISKS\n-QUALITY CERTIFICATE BY MANUFACTURER\nCONDITIONS:\nINVOICE AMOUNT MUST NOT EXCEED L/C AMOUNT\nALL DOCUMENTS IN ENGLISH\nPRESENTATION: 15 DAYS AFTER SHIPMENT\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "SKC-2024-NB-089",
        "invoice_date": "2024-07-22",
        "issued_by": "SK Chemicals Co., Ltd.",
        "issued_to": "浙江恒逸石化有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "200 Metric Tons of PET Resin Bottle Grade CB-602, Intrinsic Viscosity 0.80 dL/g, packed in 1100KG jumbo bags",
            "quantity": 200,
            "unit": "Metric Tons",
            "unit_price": 1650.00,
            "amount": 330000.00
          }
        ],
        "total_amount": 330000.00,
        "trade_terms": "CIF Ningbo",
        "raw_text": "SK chemicals\nCOMMERCIAL INVOICE\n\nInvoice No: SKC-2024-NB-089\nDate: July 22, 2024\nL/C No: LC2024-KR-156\n\nFrom: SK Chemicals Co., Ltd.\n26 Jong-ro, Jongno-gu\nSeoul 03188, Korea\nTel: +82-2-2008-2008\n\nTo: 浙江恒逸石化有限公司\n浙江省宁波市镇海区大运路168号\n电话: 0574-12345678\n\nShipped per: S.S. ONE Commitment V.089W\nFrom Busan, Korea to Ningbo, China\n\nDescription of Goods:\nPET RESIN BOTTLE GRADE CB-602\nINTRINSIC VISCOSITY 0.80 DL/G\nPACKED IN 1100KG JUMBO BAGS\n\nQuantity: 200 Metric Tons\nUnit Price: USD1,650.00/MT\nAmount: USD330,000.00\n\nTotal Amount: USD330,000.00\nSAY US DOLLARS THREE HUNDRED THIRTY THOUSAND ONLY\n\nTerms: CIF Ningbo\nPayment: By L/C at sight\n\nNote: This invoice amount exceeds L/C amount by USD10,000.00\nwhich will be settled separately by T/T.\n\nAuthorized Signature:\nKim Min-jun\nExport Manager\nSK Chemicals Co., Ltd.\n\nBANK INFO:\nSHINHAN BANK, SEOUL\nA/C: 123-45-678901\nSWIFT: SHBKKRSE"
      },
      "bill_of_lading": {
        "bl_number": "ONE-BUS-2024-2234",
        "shipper": "SK Chemicals Co., Ltd., Seoul, Korea",
        "consignee": "To Order",
        "notify_party": "宁波恒逸石化有限公司, 宁波市镇海区大运路168号",
        "vessel": "ONE Commitment",
        "voyage": "V.089W",
        "port_of_loading": "Busan, Korea",
        "port_of_discharge": "Ningbo, China",
        "onboard_date": "2024-07-23",
        "issue_date": "2024-07-24",
        "goods_description": "200 Metric Tons of PET Resin Bottle Grade CB-602, Intrinsic Viscosity 0.80±0.02 dL/g, packed in 1100KG jumbo bags",
        "number_of_packages": "200 jumbo bags",
        "gross_weight": "220 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "Ocean Network Express Pte. Ltd.",
        "raw_text": "OCEAN NETWORK EXPRESS\nBILL OF LADING\n\nB/L NO: ONE-BUS-2024-2234\nBOOKING REF: NBE240723001\n\nSHIPPER:\nSK CHEMICALS CO.,LTD.\n26 JONG-RO, JONGNO-GU\nSEOUL 03188, KOREA\n\nCONSIGNEE:\nTO ORDER\n\nNOTIFY PARTY:\nNINGBO HENGYI PETROCHEMICAL CO.,LTD.\nNO.168 DAYUN ROAD, ZHENHAI DISTRICT\nNINGBO 315200, CHINA\nTEL: 86-574-12345678\n\nPRE-CARRIAGE: N/A\nPORT OF LOADING: BUSAN, KOREA\nPORT OF DISCHARGE: NINGBO, CHINA\nPLACE OF DELIVERY: NINGBO, CHINA\n\nVESSEL: ONE COMMITMENT\nVOYAGE: V.089W\n\nCONTAINER NO: ONEU1234567\nSEAL: 123456\nMARKS & NUMBERS: N/M\n\nDESCRIPTION OF GOODS:\n200 JUMBO BAGS STC:\nPET RESIN BOTTLE GRADE CB-602\nINTRINSIC VISCOSITY 0.80±0.02 DL/G\nPACKED IN 1100KG JUMBO BAGS\nGROSS WEIGHT: 220,000 KGS\nMEASUREMENT: 450 CBM\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: BUSAN, JULY 24, 2024\n\nLOADED ON BOARD: JULY 23, 2024\n\nSIGNED BY:\n_______________\nOCEAN NETWORK EXPRESS PTE.LTD.\nAS AGENT FOR THE CARRIER\n\nCLEAN ON BOARD\nSHIPPED IN APPARENT GOOD ORDER AND CONDITION"
      },
      "insurance_policy": {
        "policy_number": "SAMSUNG-KR-2024-44567",
        "insured": "SK Chemicals Co., Ltd.",
        "insurance_amount": 352000.00,
        "currency": "USD",
        "coverage": "All Risks",
        "goods_description": "200 Metric Tons of PET Resin Bottle Grade CB-602",
        "vessel": "ONE Commitment",
        "from": "Busan, Korea",
        "to": "Ningbo, China",
        "issue_date": "2024-07-22",
        "claims_payable_at": "Ningbo, China",
        "raw_text": "SAMSUNG FIRE & MARINE INSURANCE CO.,LTD.\nMARINE CARGO INSURANCE POLICY\n\nPOLICY NO: SAMSUNG-KR-2024-44567\n\nTHE ASSURED: SK CHEMICALS CO.,LTD.\n26 JONG-RO, JONGNO-GU, SEOUL, KOREA\n\nTHIS POLICY OF INSURANCE WITNESSES THAT SAMSUNG FIRE & MARINE INSURANCE CO.,LTD. (HEREINAFTER CALLED THE COMPANY) AT THE REQUEST OF THE ASSURED NAMED ABOVE, AND IN CONSIDERATION OF THE PREMIUM PAID, UNDERTAKES TO INSURE THE UNDERMENTIONED GOODS.\n\nVOYAGE: FROM BUSAN, KOREA TO NINGBO, CHINA\nPER S.S.: ONE COMMITMENT V.089W\n\nINSURED VALUE: USD352,000.00\n(U.S.DOLLARS THREE HUNDRED FIFTY-TWO THOUSAND ONLY)\n\nDESCRIPTION OF GOODS:\n200 METRIC TONS PET RESIN BOTTLE GRADE CB-602\nPACKED IN JUMBO BAGS\n\nCONDITIONS: ALL RISKS AS PER PICC CLAUSES\n\nPREMIUM: AS ARRANGED\nDATE OF ISSUE: JULY 22, 2024\nCLAIMS PAYABLE AT: NINGBO, CHINA\n\nAUTHORIZED SIGNATURE\n\nSAMGSUNG FIRE & MARINE INSURANCE\nINTERNATIONAL DEPARTMENT\n\nTHIS POLICY IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-08-05",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Commercial Invoice",
            "field": "invoice_amount",
            "description": "发票金额USD 330,000.00超过信用证金额USD 320,000.00，且超出部分未经L/C允许",
            "ucp_reference": "UCP600 Article 18(b) - 发票金额不得超过信用证金额，除非L/C允许超额",
            "severity": "严重"
          },
          {
            "document": "Commercial Invoice",
            "field": "applicant_name",
            "description": "发票抬头为'浙江恒逸石化有限公司'，而信用证申请人为'宁波恒逸石化有限公司'，公司名称不一致",
            "ucp_reference": "UCP600 Article 18(a)(ii) - 发票必须出具给申请人或以其为抬头",
            "severity": "严重"
          }
        ],
        "overall_assessment": "存在重大不符点：发票金额超额且抬头错误。建议拒付或联系申请人接受不符点。"
      }
    },
    {
      "case_id": "case_04",
      "case_description": "提单不符点案例（纺织品：越南服装）",
      "letter_of_credit": {
        "lc_number": "LC2024-VN-334",
        "issuing_bank": "招商银行广州分行",
        "advising_bank": "越南外贸股份制商业银行胡志明市分行",
        "applicant": {
          "name": "广州时尚服装贸易有限公司",
          "address": "广州市白云区黄石东路88号"
        },
        "beneficiary": {
          "name": "Viettex Fashion Joint Stock Company",
          "address": "Lot A2, Tan Tao Industrial Zone, Binh Tan District, Ho Chi Minh City, Vietnam"
        },
        "currency": "USD",
        "amount": 87500.00,
        "amount_tolerance": "+/- 5%",
        "goods_description": "15,000 Pieces Ladies Cotton T-shirts, 100% Cotton, Style LT-2024-089, Sizes S-XL, packed in cartons",
        "latest_shipment_date": "2024-09-10",
        "expiry_date": "2024-09-30",
        "expiry_place": "Ho Chi Minh City, Vietnam",
        "presentation_period": "15 days after the date of shipment",
        "loading_port": "Ho Chi Minh City, Vietnam",
        "discharge_port": "Guangzhou, China",
        "trade_terms": "FOB Ho Chi Minh City",
        "partial_shipment": "Allowed",
        "transhipment": "Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading made out to order of issuing bank, notify applicant",
          "Packing List in 3 copies",
          "Certificate of Origin Form E"
        ],
        "additional_conditions": [
          "Bill of lading must show 'Clean On Board'",
          "Shipment must be effected before Sept 10, 2024"
        ],
        "raw_text": "DOCUMENTARY CREDIT\nCREDIT NO.: LC2024-VN-334\nISSUING BANK: CHINA MERCHANTS BANK GUANGZHOU BRANCH\nADVISING BANK: VIETNAM BANK FOR TRADE & INDUSTRY (HCM BRANCH)\nAPPLICANT:\nGUANGZHOU FASHION GARMENT TRADING CO.,LTD.\nNO.88 HUANGSHI EAST ROAD, BAIYUN DISTRICT\nGUANGZHOU 510420, CHINA\nBENEFICIARY:\nVIETTEX FASHION JOINT STOCK COMPANY\nLOT A2, TAN TAO INDUSTRIAL ZONE\nBINH TAN DISTRICT, HO CHI MINH CITY, VIETNAM\nAMOUNT: USD87,500.00 (+/-5%)\nCURRENCY: USD\nEXPIRY DATE: SEPTEMBER 30, 2024\nPLACE: HO CHI MINH CITY, VIETNAM\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: ALLOWED\nTRANSSHIPMENT: ALLOWED\nLOADING: HO CHI MINH CITY, VIETNAM\nDESTINATION: GUANGZHOU, CHINA\nLATEST SHIPMENT: SEPTEMBER 10, 2024\nTRADE TERMS: FOB HO CHI MINH CITY\nGOODS:\n15,000 PIECES LADIES COTTON T-SHIRTS\n100% COTTON, STYLE LT-2024-089\nSIZES S-XL, PACKED IN CARTONS\nDOCUMENTS REQUIRED:\n1. SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n2. FULL SET CLEAN ON BOARD B/L MADE OUT TO ORDER OF ISSUING BANK NOTIFY APPLICANT\n3. PACKING LIST IN 3 COPIES\n4. CERTIFICATE OF ORIGIN FORM E\nADDITIONAL CONDITIONS:\nB/L MUST SHOW 'CLEAN ON BOARD'\nSHIPMENT MUST BE EFFECTED BEFORE SEPT 10, 2024\nPRESENTATION: 15 DAYS AFTER SHIPMENT\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "VTF-2024-GZ-156",
        "invoice_date": "2024-09-08",
        "issued_by": "Viettex Fashion Joint Stock Company",
        "issued_to": "广州时尚服装贸易有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "15,000 Pieces Ladies Cotton T-shirts, 100% Cotton, Style LT-2024-089, Sizes S-XL, packed in cartons",
            "quantity": 15000,
            "unit": "Pieces",
            "unit_price": 5.83,
            "amount": 87450.00
          }
        ],
        "total_amount": 87450.00,
        "trade_terms": "FOB Ho Chi Minh City",
        "raw_text": "VIETTEX FASHION JOINT STOCK COMPANY\nLOT A2, TAN TAO INDUSTRIAL ZONE, HO CHI MINH CITY, VIETNAM\nTEL: +84-28-1234-5678\n\nCOMMERCIAL INVOICE\n\nInvoice No.: VTF-2024-GZ-156\nDate: September 8, 2024\nL/C No.: LC2024-VN-334\n\nSOLD TO:\nGUANGZHOU FASHION GARMENT TRADING CO.,LTD.\nNO.88 HUANGSHI EAST ROAD\nBAIYUN DISTRICT, GUANGZHOU 510420\nCHINA\n\nSHIPMENT FROM: HO CHI MINH CITY, VIETNAM\nTO: GUANGZHOU, CHINA\nBY VESSEL: HMM HELSINKI V.221E\n\n-------------------------------------------------------------------\nDESCRIPTION                              QTY        U/PRICE   AMOUNT\n-------------------------------------------------------------------\nLADIES COTTON T-SHIRTS                   15,000 PCS USD5.83   USD87,450.00\n100% COTTON, STYLE LT-2024-089\nSIZES: S-XL (S:3000, M:4500, L:4500, XL:3000)\nPACKED IN 625 CARTONS\n-------------------------------------------------------------------\nTOTAL CIF VALUE:                                    USD87,450.00\n\nSAY US DOLLARS EIGHTY-SEVEN THOUSAND FOUR HUNDRED FIFTY ONLY\n\nTERMS: FOB HO CHI MINH CITY\nORIGIN: VIETNAM\n\nBank: Vietnam Bank for Trade & Industry\nA/C No: 123456789\n\nAuthorized Signature: Nguyen Thi Mai\nGeneral Director"
      },
      "bill_of_lading": {
        "bl_number": "HMM-HCM-2024-9981",
        "shipper": "Viettex Fashion Joint Stock Company, Ho Chi Minh City, Vietnam",
        "consignee": "To Order of China Merchants Bank Guangzhou Branch",
        "notify_party": "广州时尚服装贸易有限公司, 广州市白云区黄石东路88号",
        "vessel": "HMM Helsinki",
        "voyage": "V.221E",
        "port_of_loading": "Cat Lai Port, Ho Chi Minh City, Vietnam",
        "port_of_discharge": "Guangzhou, China",
        "onboard_date": "2024-09-12",
        "issue_date": "2024-09-13",
        "goods_description": "15,000 Pieces Ladies Cotton T-shirts, Style LT-2024-089, packed in cartons - 2 cartons slightly damaged",
        "number_of_packages": "625 cartons",
        "gross_weight": "12.5 MT",
        "freight": "Freight Collect",
        "number_of_originals": "3/3",
        "clean_onboard": false,
        "carrier_signature": "HMM Co., Ltd., Ho Chi Minh Agent",
        "raw_text": "HMM CO., LTD.\nBILL OF LADING\n\nB/L NO: HMM-HCM-2024-9981\n\nSHIPPER:\nVIETTEX FASHION JOINT STOCK COMPANY\nLOT A2, TAN TAO INDUSTRIAL ZONE\nBINH TAN DISTRICT\nHO CHI MINH CITY, VIETNAM\n\nCONSIGNEE:\nTO ORDER OF CHINA MERCHANTS BANK GUANGZHOU BRANCH\n\nNOTIFY PARTY:\nGUANGZHOU FASHION GARMENT TRADING CO.,LTD.\nNO.88 HUANGSHI EAST ROAD\nBAIYUN DISTRICT, GUANGZHOU 510420, CHINA\n\nVESSEL: HMM HELSINKI\nVOYAGE: V.221E\n\nPORT OF LOADING: CAT LAI PORT, HO CHI MINH CITY, VIETNAM\nPORT OF DISCHARGE: GUANGZHOU, CHINA\nPLACE OF RECEIPT: HO CHI MINH CITY\nPLACE OF DELIVERY: GUANGZHOU\n\nCONTAINER NO: HMMU1234567\nSEAL: 789012\n\nDESCRIPTION OF PACKAGES:\n625 CARTONS STC:\nLADIES COTTON T-SHIRTS\nSTYLE LT-2024-089\n*** 2 CARTONS SLIGHTLY DAMAGED ***\nGROSS WEIGHT: 12,500 KGS\nCBM: 62.5\n\nTOTAL PACKAGES: SIX HUNDRED TWENTY-FIVE (625) CARTONS ONLY\n\nFREIGHT: COLLECT\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: HO CHI MINH CITY, SEPTEMBER 13, 2024\n\nLOADED ON BOARD DATE: SEPTEMBER 12, 2024\n\nSIGNED BY: _______________\nHMM CO.,LTD. HO CHI MINH AGENT\n\nREMARKS:\nSHIPPER'S LOAD, COUNT AND SEAL\n2 CARTONS SLIGHTLY DAMAGED - CONTENTS INTACT"
      },
      "insurance_policy": {
        "policy_number": "BAOVIET-2024-78234",
        "insured": "Viettex Fashion Joint Stock Company",
        "insurance_amount": 100000.00,
        "currency": "USD",
        "coverage": "All Risks",
        "goods_description": "15,000 Pieces Ladies Cotton T-shirts",
        "vessel": "HMM Helsinki",
        "from": "Ho Chi Minh City, Vietnam",
        "to": "Guangzhou, China",
        "issue_date": "2024-09-11",
        "claims_payable_at": "Guangzhou, China",
        "raw_text": "BAO VIET INSURANCE CORPORATION\nMARINE CARGO INSURANCE CERTIFICATE\n\nCERTIFICATE NO.: BAOVIET-2024-78234\n\nINSURED: VIETTEX FASHION JOINT STOCK COMPANY\nHO CHI MINH CITY, VIETNAM\n\nVOYAGE: HO CHI MINH CITY TO GUANGZHOU\nVESSEL: HMM HELSINKI V.221E\n\nAMOUNT INSURED: USD100,000.00\n\nINTEREST INSURED:\n15,000 PIECES LADIES COTTON T-SHIRTS\nPACKED IN 625 CARTONS\n\nCONDITIONS: ALL RISKS\n\nDATE OF ISSUE: SEPTEMBER 11, 2024\nCLAIMS PAYABLE AT: GUANGZHOU, CHINA\n\nFOR BAO VIET INSURANCE CORP.\n\nAUTHORIZED SIGNATURE\n\nTHIS CERTIFICATE IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-09-20",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Bill of Lading",
            "field": "onboard_date",
            "description": "提单显示装船日期为2024年9月12日，晚于信用证规定的最迟装运日2024年9月10日",
            "ucp_reference": "UCP600 Article 20(c) - 提单日期必须在信用证规定的装运期限内",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "clean_onboard",
            "description": "提单显示'2 cartons slightly damaged'，构成不清洁批注，不符合'Clean On Board'要求",
            "ucp_reference": "UCP600 Article 27(a) - 银行只接受清洁运输单据，未明确声明货物或包装有缺陷",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "port_of_loading",
            "description": "提单显示装货港为Cat Lai Port，虽地理上属于胡志明市，但未明确显示'Ho Chi Minh City'，存在歧义",
            "ucp_reference": "UCP600 Article 20(a)(iii) - 提单必须显示信用证规定的装货港",
            "severity": "一般"
          }
        ],
        "overall_assessment": "存在重大不符点：迟装运及不清洁提单。建议拒付。"
      }
    },
    {
      "case_id": "case_05",
      "case_description": "保险单不符点案例（电子产品：台湾芯片）",
      "letter_of_credit": {
        "lc_number": "LC2024-TW-778",
        "issuing_bank": "上海浦东发展银行苏州分行",
        "advising_bank": "国泰世华商业银行台北分行",
        "applicant": {
          "name": "苏州晶圆电子科技有限公司",
          "address": "苏州市工业园区星龙街428号"
        },
        "beneficiary": {
          "name": "Taiwan Semiconductor Trading Corp.",
          "address": "No. 168, Park Ave., Hsinchu Science Park, Hsinchu 300, Taiwan"
        },
        "currency": "USD",
        "amount": 580000.00,
        "amount_tolerance": "+/- 0%",
        "goods_description": "100,000 Units Microcontroller ICs Model STM32F407VGT6, 32-bit ARM Cortex-M4, LQFP100 package, RoHS compliant",
        "latest_shipment_date": "2024-08-31",
        "expiry_date": "2024-09-21",
        "expiry_place": "Taipei, Taiwan",
        "presentation_period": "21 days after the date of shipment",
        "loading_port": "Keelung, Taiwan",
        "discharge_port": "Shanghai, China",
        "trade_terms": "CIF Shanghai",
        "partial_shipment": "Not Allowed",
        "transhipment": "Not Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Air Waybill showing goods consigned to applicant",
          "Insurance policy for 110% of CIF value covering All Risks and War Risks",
          "Packing List in 3 copies",
          "Certificate of Origin"
        ],
        "additional_conditions": [
          "Insurance coverage must be at least 110% of invoice value",
          "Insurance currency must be same as L/C currency (USD)"
        ],
        "raw_text": "IRREVOCABLE DOCUMENTARY CREDIT\nNO.: LC2024-TW-778\nISSUING BANK: SHANGHAI PUDONG DEVELOPMENT BANK SUZHOU BRANCH\nADVISING BANK: CATHAY UNITED BANK TAIPEI BRANCH\nAPPLICANT:\nSUZHOU JINGYUAN ELECTRONICS TECH CO.,LTD.\nNO.428 XINGLONG STREET, SUZHOU INDUSTRIAL PARK\nSUZHOU 215000, CHINA\nBENEFICIARY:\nTAIWAN SEMICONDUCTOR TRADING CORP.\nNO.168, PARK AVE., HSINCHU SCIENCE PARK\nHSINCHU 300, TAIWAN\nAMOUNT: USD580,000.00 (NO TOLERANCE)\nEXPIRY DATE: SEPTEMBER 21, 2024\nPLACE: TAIPEI, TAIWAN\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: NOT ALLOWED\nTRANSSHIPMENT: NOT ALLOWED\nLOADING: KEELUNG, TAIWAN\nDESTINATION: SHANGHAI, CHINA\nLATEST SHIPMENT: AUGUST 31, 2024\nTRADE TERMS: CIF SHANGHAI\nGOODS:\n100,000 UNITS MICROCONTROLLER ICs MODEL STM32F407VGT6\n32-BIT ARM CORTEX-M4, LQFP100 PACKAGE, ROHS COMPLIANT\nDOCUMENTS REQUIRED:\n-SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n-AIR WAYBILL CONSIGNED TO APPLICANT\n-INSURANCE POLICY 110% OF CIF COVERING ALL RISKS AND WAR RISKS\n-PACKING LIST IN 3 COPIES\n-CERTIFICATE OF ORIGIN\nCONDITIONS:\nINSURANCE MUST BE 110% OF INVOICE VALUE\nINSURANCE CURRENCY MUST BE USD\nPRESENTATION: 21 DAYS AFTER SHIPMENT\nUCP600 APPLICABLE"
      },
      "commercial_invoice": {
        "invoice_number": "TSMC-2024-SZ-445",
        "invoice_date": "2024-08-25",
        "issued_by": "Taiwan Semiconductor Trading Corp.",
        "issued_to": "苏州晶圆电子科技有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "100,000 Units Microcontroller ICs Model STM32F407VGT6, 32-bit ARM Cortex-M4, LQFP100 package, RoHS compliant",
            "quantity": 100000,
            "unit": "Units",
            "unit_price": 5.80,
            "amount": 580000.00
          }
        ],
        "total_amount": 580000.00,
        "trade_terms": "CIF Shanghai",
        "raw_text": "TAIWAN SEMICONDUCTOR TRADING CORP.\nNO.168, PARK AVE., HSINCHU SCIENCE PARK\nHSINCHU 300, TAIWAN\n\nCOMMERCIAL INVOICE\n\nInvoice No: TSMC-2024-SZ-445\nDate: August 25, 2024\nL/C No: LC2024-TW-778\n\nTo:\nSUZHOU JINGYUAN ELECTRONICS TECH CO.,LTD.\nNO.428 XINGLONG STREET\nSUZHOU INDUSTRIAL PARK, SUZHOU 215000\nCHINA\n\nFrom: Hsinchu, Taiwan\nTo: Shanghai, China\nBy: China Airlines CI-501\n\nDescription of Goods:\n100,000 Units Microcontroller ICs\nModel: STM32F407VGT6\n32-bit ARM Cortex-M4\nLQFP100 package, RoHS compliant\nPacked in anti-static trays and cartons\n\nQuantity: 100,000 Units\nUnit Price: USD5.80\nAmount: USD580,000.00\n\nTotal: USD580,000.00\nSAY US DOLLARS FIVE HUNDRED EIGHTY THOUSAND ONLY\n\nTerms: CIF Shanghai\n\nAuthorized Signature:\nDavid Chen\nPresident\n\nBank:\nCATHAY UNITED BANK, TAIPEI\nA/C: 123456789012\nSWIFT: UBOTTWTP"
      },
      "bill_of_lading": {
        "bl_number": "CI-KEL-2024-5567",
        "shipper": "Taiwan Semiconductor Trading Corp., Hsinchu, Taiwan",
        "consignee": "苏州晶圆电子科技有限公司",
        "notify_party": "苏州晶圆电子科技有限公司",
        "vessel": "China Airlines CI-501",
        "voyage": "N/A",
        "port_of_loading": "Taiwan Taoyuan International Airport (TPE)",
        "port_of_discharge": "Shanghai Pudong International Airport (PVG)",
        "onboard_date": "2024-08-28",
        "issue_date": "2024-08-28",
        "goods_description": "100,000 Units Microcontroller ICs Model STM32F407VGT6, packed in anti-static trays and cartons",
        "number_of_packages": "50 cartons",
        "gross_weight": "850 KGS",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "China Airlines Cargo",
        "raw_text": "CHINA AIRLINES\nAIR WAYBILL\n\nAWB NO: CI-KEL-2024-5567\n\nSHIPPER:\nTAIWAN SEMICONDUCTOR TRADING CORP.\nNO.168, PARK AVE., HSINCHU SCIENCE PARK\nHSINCHU 300, TAIWAN\nTEL: +886-3-1234567\n\nCONSIGNEE:\nSUZHOU JINGYUAN ELECTRONICS TECH CO.,LTD.\nNO.428 XINGLONG STREET, SUZHOU INDUSTRIAL PARK\nSUZHOU 215000, CHINA\n\nNOTIFY PARTY:\nSAME AS CONSIGNEE\n\nISSUING CARRIER: CHINA AIRLINES\nFLIGHT/ DATE: CI-501 / AUGUST 28, 2024\n\nAIRPORT OF DEPARTURE: TAIWAN TAOYUAN INT'L AIRPORT (TPE)\nAIRPORT OF DESTINATION: SHANGHAI PUDONG INT'L AIRPORT (PVG)\n\nHANDLING INFORMATION:\nFRAGILE ELECTRONIC COMPONENTS\nKEEP DRY\n\nDESCRIPTION OF GOODS:\n50 CARTONS STC:\n100,000 UNITS MICROCONTROLLER ICs\nMODEL STM32F407VGT6\nIN ANTI-STATIC TRAYS\n\nGROSS WEIGHT: 850 KGS\nCHARGEABLE WEIGHT: 850 KGS\nRATE: AS AGREED\nFREIGHT: PREPAID\n\nEXECUTED ON: AUGUST 28, 2024\nAT: TAIPEI, TAIWAN\n\nSIGNATURE OF ISSUING CARRIER:\n_____________________\nCHINA AIRLINES CARGO\n\nORIGINAL 3 (FOR SHIPPER)"
      },
      "insurance_policy": {
        "policy_number": "CATHAY-TW-2024-99012",
        "insured": "Taiwan Semiconductor Trading Corp.",
        "insurance_amount": 580000.00,
        "currency": "TWD",
        "coverage": "All Risks",
        "goods_description": "100,000 Units Microcontroller ICs",
        "vessel": "China Airlines CI-501",
        "from": "Taipei, Taiwan",
        "to": "Shanghai, China",
        "issue_date": "2024-08-29",
        "claims_payable_at": "Taipei, Taiwan",
        "raw_text": "CATHAY LIFE INSURANCE CO., LTD.\nMARINE CARGO INSURANCE POLICY\n\nPOLICY NO.: CATHAY-TW-2024-99012\n\nINSURED: TAIWAN SEMICONDUCTOR TRADING CORP.\nHSINCHU, TAIWAN\n\nL/C NO.: LC2024-TW-778\n\nTHIS POLICY WITNESSES THAT CATHAY LIFE INSURANCE CO., LTD. (HEREINAFTER CALLED THE COMPANY) AT THE REQUEST OF THE INSURED, UNDERTAKES TO INSURE THE UNDERMENTIONED GOODS.\n\nVOYAGE: FROM TAIPEI, TAIWAN TO SHANGHAI, CHINA\nPER CONVEYANCE: CHINA AIRLINES CI-501\n\nINSURED VALUE: TWD580,000.00\n(NEW TAIWAN DOLLARS FIVE HUNDRED EIGHTY THOUSAND ONLY)\n\nDESCRIPTION OF GOODS:\n100,000 UNITS MICROCONTROLLER ICs\nPACKED IN CARTONS\n\nPREMIUM: AS ARRANGED\nDATE OF ISSUE: AUGUST 29, 2024\n\nCONDITIONS: ALL RISKS\n\nCLAIMS PAYABLE AT: TAIPEI, TAIWAN\n\nAUTHORIZED SIGNATURE:\n________________\nCATAY LIFE INSURANCE CO., LTD.\n\nNOTE: INSURANCE EFFECTED IN TWD CURRENCY\nCONVERSION RATE TO USD APPROX. 31.5:1\n\nTHIS POLICY IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-09-10",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Insurance Policy",
            "field": "insurance_amount",
            "description": "保险金额为TWD 580,000.00，按汇率换算仅约USD 18,000，远低于CIF价值的110%（应为USD 638,000），且币种错误",
            "ucp_reference": "UCP600 Article 28(f)(ii) - 保险金额必须至少为发票金额的110%，且币种须与信用证一致",
            "severity": "严重"
          },
          {
            "document": "Insurance Policy",
            "field": "issue_date",
            "description": "保险单签发日期为2024年8月29日，晚于装运日期2024年8月28日，除非保险单明确表明保险责任不迟于装运日生效",
            "ucp_reference": "UCP600 Article 28(e) - 保险单日期不得晚于装运日期，除非表明保险责任最迟于装运日生效",
            "severity": "严重"
          },
          {
            "document": "Insurance Policy",
            "field": "coverage",
            "description": "保险单仅显示'All Risks'，未显示信用证要求的'War Risks'（战争险）",
            "ucp_reference": "UCP600 Article 28(a) - 保险单必须涵盖信用证要求的险别",
            "severity": "严重"
          }
        ],
        "overall_assessment": "存在多项重大不符点：保险金额严重不足、币种错误、缺战争险、倒签保单。建议拒付。"
      }
    },
    {
      "case_id": "case_06",
      "case_description": "交单时间不符点案例（农产品：泰国香米）",
      "letter_of_credit": {
        "lc_number": "LC2024-TH-445",
        "issuing_bank": "中国工商银行厦门分行",
        "advising_bank": "盘谷银行曼谷分行",
        "applicant": {
          "name": "厦门金象进出口贸易有限公司",
          "address": "厦门市思明区鹭江道52号"
        },
        "beneficiary": {
          "name": "Thai Rice Export Co., Ltd.",
          "address": "1250 Charoen Krung Road, Bang Rak, Bangkok 10500, Thailand"
        },
        "currency": "USD",
        "amount": 245000.00,
        "amount_tolerance": "+/- 5%",
        "goods_description": "500 Metric Tons Thai Hom Mali Rice (Jasmine Rice), White Rice 100% Grade A, Crop 2024, packed in 25KG new PP bags",
        "latest_shipment_date": "2024-07-20",
        "expiry_date": "2024-08-10",
        "expiry_place": "Bangkok, Thailand",
        "presentation_period": "21 days after the date of shipment but within the validity of this credit",
        "loading_port": "Bangkok, Thailand",
        "discharge_port": "Xiamen, China",
        "trade_terms": "CIF Xiamen",
        "partial_shipment": "Allowed",
        "transhipment": "Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading made out to order, marked freight prepaid, notify applicant",
          "Insurance policy for 110% of CIF value covering All Risks",
          "Quality Certificate issued by Department of Foreign Trade",
          "Phytosanitary Certificate"
        ],
        "additional_conditions": [
          "Documents must be presented not later than 21 days after B/L date",
          "Latest date of presentation: August 10, 2024"
        ],
        "raw_text": "IRREVOCABLE DOCUMENTARY CREDIT\nNUMBER: LC2024-TH-445\nISSUING BANK: ICBC XIAMEN BRANCH\nADVISING BANK: BANGKOK BANK PUBLIC CO., LTD.\nAPPLICANT:\nXIAMEN GOLDEN ELEPHANT IMPORT & EXPORT TRADING CO.,LTD.\nNO.52 LUJIANG ROAD, SIMING DISTRICT\nXIAMEN 361001, CHINA\nBENEFICIARY:\nTHAI RICE EXPORT CO., LTD.\n1250 CHAROEN KRUNG ROAD, BANG RAK\nBANGKOK 10500, THAILAND\nAMOUNT: USD245,000.00 (+/-5%)\nCURRENCY: USD\nEXPIRY DATE: AUGUST 10, 2024\nPLACE: BANGKOK, THAILAND\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: ALLOWED\nTRANSSHIPMENT: ALLOWED\nLOADING: BANGKOK, THAILAND\nDESTINATION: XIAMEN, CHINA\nLATEST SHIPMENT: JULY 20, 2024\nTRADE TERMS: CIF XIAMEN\nGOODS:\n500 METRIC TONS THAI HOM MALI RICE (JASMINE RICE)\nWHITE RICE 100% GRADE A, CROP 2024\nPACKED IN 25KG NEW PP BAGS\nDOCUMENTS REQUIRED:\n-SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n-FULL SET CLEAN ON BOARD B/L TO ORDER\n-FREIGHT PREPAID, NOTIFY APPLICANT\n-INSURANCE POLICY 110% OF CIF COVERING ALL RISKS\n-QUALITY CERTIFICATE BY DEPT OF FOREIGN TRADE\n-PHYTOSANITARY CERTIFICATE\nCONDITIONS:\nDOCUMENTS MUST BE PRESENTED WITHIN 21 DAYS AFTER B/L DATE\nLATEST PRESENTATION: AUGUST 10, 2024\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "TRE-2024-XM-223",
        "invoice_date": "2024-07-18",
        "issued_by": "Thai Rice Export Co., Ltd.",
        "issued_to": "厦门金象进出口贸易有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "500 Metric Tons Thai Hom Mali Rice (Jasmine Rice), White Rice 100% Grade A, Crop 2024, packed in 25KG new PP bags",
            "quantity": 500,
            "unit": "Metric Tons",
            "unit_price": 490.00,
            "amount": 245000.00
          }
        ],
        "total_amount": 245000.00,
        "trade_terms": "CIF Xiamen",
        "raw_text": "THAI RICE EXPORT CO., LTD.\n1250 CHAROEN KRUNG ROAD, BANGKOK 10500, THAILAND\nTEL: +66-2-123-4567\n\nCOMMERCIAL INVOICE\n\nInvoice No: TRE-2024-XM-223\nDate: July 18, 2024\nL/C No: LC2024-TH-445\n\nBuyer:\nXIAMEN GOLDEN ELEPHANT IMPORT & EXPORT TRADING CO.,LTD.\nNO.52 LUJIANG ROAD, SIMING DISTRICT\nXIAMEN 361001, CHINA\n\nShipped by: S.S. Regional Container Lines V.445N\nFrom Bangkok, Thailand to Xiamen, China\n\nDescription:\nThai Hom Mali Rice (Jasmine Rice)\nWhite Rice 100% Grade A, Crop 2024\nPacked in 25KG new PP bags\n\nQuantity: 500 Metric Tons\nUnit Price: USD490.00/MT\nTotal Amount: USD245,000.00\n\nSAY US DOLLARS TWO HUNDRED FORTY-FIVE THOUSAND ONLY\n\nTerms: CIF Xiamen\nOrigin: Thailand\n\nAuthorized Signature:\nSomchai Jaidee\nManaging Director\n\nBank: Bangkok Bank Public Co., Ltd.\nA/C: 123-4-56789-0\nSWIFT: BKKBTHBK"
      },
      "bill_of_lading": {
        "bl_number": "RCL-BKK-2024-3341",
        "shipper": "Thai Rice Export Co., Ltd., Bangkok, Thailand",
        "consignee": "To Order",
        "notify_party": "厦门金象进出口贸易有限公司, 厦门市思明区鹭江道52号",
        "vessel": "Regional Container Lines",
        "voyage": "V.445N",
        "port_of_loading": "Bangkok, Thailand",
        "port_of_discharge": "Xiamen, China",
        "onboard_date": "2024-07-19",
        "issue_date": "2024-07-20",
        "goods_description": "500 Metric Tons Thai Hom Mali Rice (Jasmine Rice), White Rice 100% Grade A, Crop 2024, packed in 25KG new PP bags",
        "number_of_packages": "20000 bags",
        "gross_weight": "500 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "RCL Agencies (Thailand) Ltd.",
        "raw_text": "REGIONAL CONTAINER LINES\nBILL OF LADING\n\nB/L NO: RCL-BKK-2024-3341\n\nSHIPPER:\nTHAI RICE EXPORT CO., LTD.\n1250 CHAROEN KRUNG ROAD\nBANG RAK, BANGKOK 10500\nTHAILAND\n\nCONSIGNEE:\nTO ORDER\n\nNOTIFY PARTY:\nXIAMEN GOLDEN ELEPHANT IMPORT & EXPORT TRADING CO.,LTD.\nNO.52 LUJIANG ROAD, SIMING DISTRICT\nXIAMEN 361001, CHINA\n\nVESSEL: REGIONAL CONTAINER LINES\nVOYAGE: V.445N\n\nPORT OF LOADING: BANGKOK, THAILAND\nPORT OF DISCHARGE: XIAMEN, CHINA\nPLACE OF RECEIPT: BANGKOK\nPLACE OF DELIVERY: XIAMEN\n\nDESCRIPTION OF GOODS:\n20,000 BAGS STC:\nTHAI HOM MALI RICE (JASMINE RICE)\nWHITE RICE 100% GRADE A, CROP 2024\nPACKED IN 25KG NEW PP BAGS\n\nGROSS WEIGHT: 500,000 KGS (500 MT)\nMEASUREMENT: 1,000 CBM\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: BANGKOK, JULY 20, 2024\n\nLOADED ON BOARD DATE: JULY 19, 2024\n\nSIGNED BY:\n___________________\nRCL AGENCIES (THAILAND) LTD.\nAS AGENT FOR THE CARRIER\n\nCLEAN ON BOARD\nSHIPPED IN APPARENT GOOD ORDER AND CONDITION"
      },
      "insurance_policy": {
        "policy_number": "THAIINS-2024-55678",
        "insured": "Thai Rice Export Co., Ltd.",
        "insurance_amount": 269500.00,
        "currency": "USD",
        "coverage": "All Risks",
        "goods_description": "500 Metric Tons Thai Hom Mali Rice",
        "vessel": "Regional Container Lines",
        "from": "Bangkok, Thailand",
        "to": "Xiamen, China",
        "issue_date": "2024-07-18",
        "claims_payable_at": "Xiamen, China",
        "raw_text": "THAI INSURANCE PUBLIC COMPANY LIMITED\nMARINE CARGO INSURANCE POLICY\n\nPOLICY NO: THAIINS-2024-55678\n\nTHE INSURED: THAI RICE EXPORT CO., LTD.\nBANGKOK, THAILAND\n\nVOYAGE: FROM BANGKOK, THAILAND TO XIAMEN, CHINA\nPER S.S.: REGIONAL CONTAINER LINES V.445N\n\nSUM INSURED: USD269,500.00\n(U.S.DOLLARS TWO HUNDRED SIXTY-NINE THOUSAND FIVE HUNDRED ONLY)\n\nINTEREST INSURED:\n500 METRIC TONS THAI HOM MALI RICE\nPACKED IN 25KG PP BAGS\n\nPREMIUM: AS ARRANGED\nDATE OF ISSUE: JULY 18, 2024\n\nCONDITIONS: ALL RISKS\n\nCLAIMS PAYABLE AT: XIAMEN, CHINA\n\nFOR THAI INSURANCE PCL.\n\nAUTHORIZED SIGNATURE\n\nTHIS POLICY IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-08-15",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Presentation",
            "field": "presentation_date",
            "description": "交单日期为2024年8月15日，超过提单日期（2024年7月20日）后21天（应不晚于2024年8月10日），且超过信用证到期日（2024年8月10日）",
            "ucp_reference": "UCP600 Article 14(c) - 单据必须在信用证有效期内提交，且不得迟于装运日后21个日历日",
            "severity": "严重"
          },
          {
            "document": "Presentation",
            "field": "expiry_date",
            "description": "单据提交日晚于信用证到期日，信用证已失效",
            "ucp_reference": "UCP600 Article 6(d)(i) - 信用证必须规定一个承付或议付的到期日",
            "severity": "严重"
          }
        ],
        "overall_assessment": "存在致命不符点：迟交单且超过信用证有效期。信用证已失效，建议拒付。"
      }
    },
    {
      "case_id": "case_07",
      "case_description": "单据间相互矛盾案例（矿产品：澳大利亚铁矿石）",
      "letter_of_credit": {
        "lc_number": "LC2024-AU-889",
        "issuing_bank": "交通银行唐山分行",
        "advising_bank": "澳大利亚联邦银行珀斯分行",
        "applicant": {
          "name": "唐山钢铁集团有限公司",
          "address": "唐山市路北区建设北路15号"
        },
        "beneficiary": {
          "name": "Pilbara Minerals Export Pty Ltd",
          "address": "Level 25, 140 St Georges Terrace, Perth WA 6000, Australia"
        },
        "currency": "USD",
        "amount": 2800000.00,
        "amount_tolerance": "+/- 10%",
        "goods_description": "50,000 Wet Metric Tons of Iron Ore Fines, Fe 62% basis, typical specs: Fe 61.5%, SiO2 3.5%, Al2O3 2.5%, P 0.08% max, packed in bulk",
        "latest_shipment_date": "2024-06-30",
        "expiry_date": "2024-07-21",
        "expiry_place": "Perth, Australia",
        "presentation_period": "21 days after the date of shipment",
        "loading_port": "Port Hedland, Australia",
        "discharge_port": "Tangshan, China (Caofeidian Port)",
        "trade_terms": "CFR Tangshan",
        "partial_shipment": "Not Allowed",
        "transhipment": "Not Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading consigned to applicant",
          "Quality Certificate issued by SGS",
          "Weight Certificate issued by CIQ at loading port"
        ],
        "additional_conditions": [
          "All documents must show identical goods description and quantity",
          "Certificate of Origin required"
        ],
        "raw_text": "DOCUMENTARY CREDIT\nNO.: LC2024-AU-889\nISSUING BANK: BANK OF COMMUNICATIONS TANGSHAN BRANCH\nADVISING BANK: COMMONWEALTH BANK OF AUSTRALIA PERTH BRANCH\nAPPLICANT:\nTANGSHAN IRON & STEEL GROUP CO.,LTD.\nNO.15 JIANSHE NORTH ROAD, LUBEI DISTRICT\nTANGSHAN 063000, CHINA\nBENEFICIARY:\nPILBARA MINERALS EXPORT PTY LTD\nLEVEL 25, 140 ST GEORGES TERRACE\nPERTH WA 6000, AUSTRALIA\nAMOUNT: USD2,800,000.00 (+/-10%)\nEXPIRY DATE: JULY 21, 2024\nPLACE: PERTH, AUSTRALIA\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: NOT ALLOWED\nTRANSSHIPMENT: NOT ALLOWED\nLOADING: PORT HEDLAND, AUSTRALIA\nDESTINATION: TANGSHAN, CHINA (CAOFEIDIAN PORT)\nLATEST SHIPMENT: JUNE 30, 2024\nTRADE TERMS: CFR TANGSHAN\nGOODS:\n50,000 WET METRIC TONS OF IRON ORE FINES\nFE 62% BASIS, TYPICAL SPECS: FE 61.5%, SIO2 3.5%, AL2O3 2.5%, P 0.08% MAX\nPACKED IN BULK\nDOCUMENTS REQUIRED:\n-SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n-FULL SET CLEAN ON BOARD B/L CONSIGNED TO APPLICANT\n-QUALITY CERTIFICATE ISSUED BY SGS\n-WEIGHT CERTIFICATE ISSUED BY CIQ AT LOADING PORT\nCONDITIONS:\nALL DOCUMENTS MUST SHOW IDENTICAL GOODS DESCRIPTION AND QUANTITY\nCERTIFICATE OF ORIGIN REQUIRED\nPRESENTATION: 21 DAYS AFTER SHIPMENT\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "PME-2024-TS-778",
        "invoice_date": "2024-06-28",
        "issued_by": "Pilbara Minerals Export Pty Ltd",
        "issued_to": "唐山钢铁集团有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "50,000 Wet Metric Tons of Iron Ore Fines, Fe 62% basis, Fe 61.5%, SiO2 3.5%, Al2O3 2.5%, packed in bulk",
            "quantity": 50000,
            "unit": "Wet Metric Tons",
            "unit_price": 56.00,
            "amount": 2800000.00
          }
        ],
        "total_amount": 2800000.00,
        "trade_terms": "CFR Tangshan",
        "raw_text": "PILBARA MINERALS EXPORT PTY LTD\nLEVEL 25, 140 ST GEORGES TERRACE\nPERTH WA 6000, AUSTRALIA\nABN: 12 345 678 901\n\nTAX INVOICE / COMMERCIAL INVOICE\n\nInvoice No: PME-2024-TS-778\nDate: June 28, 2024\nL/C No: LC2024-AU-889\n\nTo:\nTANGSHAN IRON & STEEL GROUP CO.,LTD.\nNO.15 JIANSHE NORTH ROAD\nLUBEI DISTRICT, TANGSHAN 063000\nCHINA\n\nVessel: FMG Northern Spirit V.114S\nLoading: Port Hedland, Australia\nDestination: Tangshan, China\n\nDescription of Goods:\nIron Ore Fines\nFe 62% basis, Fe 61.5%, SiO2 3.5%, Al2O3 2.5%\nPacked in bulk\n\nQuantity: 50,000 Wet Metric Tons\nUnit Price: USD56.00/WMT\nTotal Value: USD2,800,000.00\n\nSAY US DOLLARS TWO MILLION EIGHT HUNDRED THOUSAND ONLY\n\nTerms: CFR Tangshan\nOrigin: Australia (Pilbara Region)\n\nAuthorized Signature:\nMichael Thompson\nCommercial Manager\n\nBank:\nCommonwealth Bank of Australia\nBSB: 062-000\nA/C: 1234 5678\nSWIFT: CTBAAU2S"
      },
      "bill_of_lading": {
        "bl_number": "FMG-PHE-2024-9923",
        "shipper": "Pilbara Minerals Export Pty Ltd, Perth, Australia",
        "consignee": "唐山钢铁集团有限公司",
        "notify_party": "唐山钢铁集团有限公司",
        "vessel": "FMG Northern Spirit",
        "voyage": "V.114S",
        "port_of_loading": "Port Hedland, Australia",
        "port_of_discharge": "Qingdao, China",
        "onboard_date": "2024-06-29",
        "issue_date": "2024-06-30",
        "goods_description": "48,500 Wet Metric Tons of Iron Ore Concentrate Pellets, Fe 65%, packed in bulk",
        "number_of_packages": "In Bulk",
        "gross_weight": "48500 WMT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "Fortescue Metals Group, Port Hedland",
        "raw_text": "FORTESCUE METALS GROUP LTD.\nBILL OF LADING\n\nB/L NO: FMG-PHE-2024-9923\n\nSHIPPER:\nPILBARA MINERALS EXPORT PTY LTD\nPERTH, WESTERN AUSTRALIA\n\nCONSIGNEE:\nTANGSHAN IRON & STEEL GROUP CO.,LTD.\nTANGSHAN, CHINA\n\nNOTIFY PARTY:\nSAME AS CONSIGNEE\n\nVESSEL: FMG NORTHERN SPIRIT\nVOYAGE: V.114S\n\nPORT OF LOADING: PORT HEDLAND, AUSTRALIA\nPORT OF DISCHARGE: QINGDAO, CHINA\n\nDESCRIPTION OF GOODS:\n48,500 WET METRIC TONS OF\nIRON ORE CONCENTRATE PELLETS\nFE 65%\nPACKED IN BULK\n\nGROSS WEIGHT: 48,500 WMT\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: PORT HEDLAND, JUNE 30, 2024\n\nLOADED ON BOARD DATE: JUNE 29, 2024\n\nSIGNED BY:\n________________\nFORTESCUE METALS GROUP\nPORT HEDLAND OPERATIONS\n\nCLEAN ON BOARD"
      },
      "insurance_policy": {
        "policy_number": "QBE-AU-2024-77834",
        "insured": "Pilbara Minerals Export Pty Ltd",
        "insurance_amount": 3080000.00,
        "currency": "USD",
        "coverage": "All Risks",
        "goods_description": "50,000 Wet Metric Tons of Iron Ore Fines",
        "vessel": "FMG Northern Spirit",
        "from": "Port Hedland, Australia",
        "to": "Tangshan, China",
        "issue_date": "2024-06-28",
        "claims_payable_at": "Tangshan, China",
        "raw_text": "QBE INSURANCE (AUSTRALIA) LIMITED\nMARINE CARGO INSURANCE CERTIFICATE\n\nCERTIFICATE NO: QBE-AU-2024-77834\n\nINSURED: PILBARA MINERALS EXPORT PTY LTD\nPERTH, WESTERN AUSTRALIA\n\nVOYAGE: PORT HEDLAND, AUSTRALIA TO TANGSHAN, CHINA\nVESSEL: FMG NORTHERN SPIRIT V.114S\n\nINSURED VALUE: USD3,080,000.00\n(U.S.DOLLARS THREE MILLION EIGHTY THOUSAND ONLY)\n\nINTEREST INSURED:\n50,000 WET METRIC TONS OF IRON ORE FINES\n\nCONDITIONS: ALL RISKS\n\nDATE OF ISSUE: JUNE 28, 2024\nCLAIMS PAYABLE AT: TANGSHAN, CHINA\n\nFOR QBE INSURANCE (AUSTRALIA) LTD.\n\nAUTHORIZED SIGNATURE\n\nTHIS CERTIFICATE IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-07-15",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Multiple Documents",
            "field": "goods_description",
            "description": "发票显示货物为'Iron Ore Fines'（铁矿石粉），提单显示为'Iron Ore Concentrate Pellets'（铁矿石球团），货物描述不一致；发票显示Fe含量62% basis，提单显示65%",
            "ucp_reference": "UCP600 Article 14(d) - 单据中的货物描述不得与信用证规定矛盾，且单据之间不得互相矛盾",
            "severity": "严重"
          },
          {
            "document": "Multiple Documents",
            "field": "quantity",
            "description": "发票数量50,000 WMT，提单数量48,500 WMT，数量差异1,500 WMT（3%），超出合理范围且未在允许溢短装范围内明确说明",
            "ucp_reference": "UCP600 Article 30(b) - 在信用证未以包装单位或个体计数时，允许5%的溢短装，但信用证规定货物数量不得超额或减少",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "port_of_discharge",
            "description": "提单显示卸货港为青岛，信用证要求为唐山（曹妃甸港），港口不一致",
            "ucp_reference": "UCP600 Article 20(a)(iii) - 提单必须显示信用证规定的卸货港",
            "severity": "严重"
          },
          {
            "document": "Multiple Documents",
            "field": "consistency",
            "description": "发票、提单、保单三份单据对货物名称、规格、卸货港的描述均存在矛盾",
            "ucp_reference": "UCP600 Article 14(d) - 单据之间不得互相矛盾",
            "severity": "严重"
          }
        ],
        "overall_assessment": "存在多项单据间矛盾：货描不一致、数量差异、港口不符。建议拒付。"
      }
    },
    {
      "case_id": "case_08",
      "case_description": "多种单据同时存在不符点案例（化工产品：沙特聚乙烯）",
      "letter_of_credit": {
        "lc_number": "LC2024-SA-556",
        "issuing_bank": "中信银行天津分行",
        "advising_bank": "利雅得银行达曼分行",
        "applicant": {
          "name": "天津渤海化工进出口有限公司",
          "address": "天津市滨海新区大港石化路88号"
        },
        "beneficiary": {
          "name": "SABIC Trading Company",
          "address": "P.O. Box 5101, Riyadh 11422, Kingdom of Saudi Arabia"
        },
        "currency": "USD",
        "amount": 450000.00,
        "amount_tolerance": "+/- 0%",
        "goods_description": "200 Metric Tons of Linear Low Density Polyethylene (LLDPE), Grade 218W, MFI 2.0 g/10min, Density 0.918 g/cm3, packed in 25KG bags",
        "latest_shipment_date": "2024-08-20",
        "expiry_date": "2024-09-10",
        "expiry_place": "Dammam, Saudi Arabia",
        "presentation_period": "21 days after the date of shipment",
        "loading_port": "Dammam, Saudi Arabia",
        "discharge_port": "Tianjin, China",
        "trade_terms": "CIF Tianjin",
        "partial_shipment": "Not Allowed",
        "transhipment": "Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading made out to order, marked freight prepaid, notify applicant",
          "Insurance policy for 110% of CIF value covering All Risks and War Risks",
          "Certificate of Origin issued by Chamber of Commerce",
          "Quality Certificate issued by manufacturer"
        ],
        "additional_conditions": [
          "Invoice amount must exactly match L/C amount",
          "Bill of lading must show 'Clean On Board'"
        ],
        "raw_text": "IRREVOCABLE DOCUMENTARY CREDIT\nNUMBER: LC2024-SA-556\nISSUING BANK: CHINA CITIC BANK TIANJIN BRANCH\nADVISING BANK: RIYAD BANK, DAMMAM BRANCH\nAPPLICANT:\nTIANJIN BOHAI CHEMICAL IMPORT & EXPORT CO.,LTD.\nNO.88 DAGANG PETROCHEMICAL ROAD\nBINHAI NEW AREA, TIANJIN 300270, CHINA\nBENEFICIARY:\nSABIC TRADING COMPANY\nP.O. BOX 5101\nRIYADH 11422\nKINGDOM OF SAUDI ARABIA\nAMOUNT: USD450,000.00 (ZERO TOLERANCE)\nEXPIRY DATE: SEPTEMBER 10, 2024\nPLACE: DAMMAM, SAUDI ARABIA\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: NOT ALLOWED\nTRANSSHIPMENT: ALLOWED\nLOADING: DAMMAM, SAUDI ARABIA\nDESTINATION: TIANJIN, CHINA\nLATEST SHIPMENT: AUGUST 20, 2024\nTRADE TERMS: CIF TIANJIN\nGOODS:\n200 METRIC TONS OF LINEAR LOW DENSITY POLYETHYLENE (LLDPE)\nGRADE 218W, MFI 2.0 G/10MIN, DENSITY 0.918 G/CM3\nPACKED IN 25KG BAGS\nDOCUMENTS REQUIRED:\n1. SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n2. FULL SET CLEAN ON BOARD B/L MADE OUT TO ORDER\n   FREIGHT PREPAID, NOTIFY APPLICANT\n3. INSURANCE POLICY 110% OF CIF COVERING ALL RISKS AND WAR RISKS\n4. CERTIFICATE OF ORIGIN ISSUED BY CHAMBER OF COMMERCE\n5. QUALITY CERTIFICATE ISSUED BY MANUFACTURER\nCONDITIONS:\nINVOICE AMOUNT MUST EXACTLY MATCH L/C AMOUNT\nB/L MUST SHOW 'CLEAN ON BOARD'\nPRESENTATION: 21 DAYS AFTER SHIPMENT\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "STC-2024-TJ-334",
        "invoice_date": "2024-08-18",
        "issued_by": "SABIC Trading Company",
        "issued_to": "天津渤海化工进出口有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "200 Metric Tons of Linear Low Density Polyethylene (LLDPE), Grade 218W, MFI 2.0 g/10min, packed in 25KG bags",
            "quantity": 200,
            "unit": "Metric Tons",
            "unit_price": 2300.00,
            "amount": 460000.00
          }
        ],
        "total_amount": 460000.00,
        "trade_terms": "CIF Tianjin",
        "raw_text": "SABIC\nSaudi Basic Industries Corporation\n\nCOMMERCIAL INVOICE\n\nInvoice No: STC-2024-TJ-334\nDate: August 18, 2024\nL/C No: LC2024-SA-556\n\nSold to:\nTIANJIN BOHAI CHEMICAL IMPORT & EXPORT CO.,LTD.\nNO.88 DAGANG PETROCHEMICAL ROAD\nBINHAI NEW AREA, TIANJIN 300270\nCHINA\n\nShipped by: MSC Rania V.445E\nFrom Dammam, Saudi Arabia\n\nProduct: LINEAR LOW DENSITY POLYETHYLENE (LLDPE)\nGrade: 218W\nMFI: 2.0 g/10min\nDensity: 0.918 g/cm3\n\nQuantity: 200 Metric Tons\nUnit Price: USD2,300.00/MT\nTotal Amount: USD460,000.00\n\nSAY US DOLLARS FOUR HUNDRED SIXTY THOUSAND ONLY\n\nTerms: CIF Tianjin\nPacking: 25KG bags (8,000 bags total)\nOrigin: Saudi Arabia\n\nNote: Price adjusted due to market fluctuation\n\nAuthorized Signature:\nAhmed Al-Rashid\nSales Manager\n\nBank: Riyad Bank\nA/C: SA123456789012345678901\nSWIFT: RIBLSARI"
      },
      "bill_of_lading": {
        "bl_number": "MSC-DAM-2024-7789",
        "shipper": "SABIC Trading Company, Riyadh, Saudi Arabia",
        "consignee": "To Order",
        "notify_party": "天津渤海化工进出口有限公司, 天津市滨海新区大港石化路88号",
        "vessel": "MSC Rania",
        "voyage": "V.445E",
        "port_of_loading": "Dammam, Saudi Arabia",
        "port_of_discharge": "Dalian, China",
        "onboard_date": "2024-08-22",
        "issue_date": "2024-08-23",
        "goods_description": "200 Metric Tons of LLDPE Grade 218W, packed in 25KG bags",
        "number_of_packages": "8000 bags",
        "gross_weight": "200 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "MSC Agency Saudi Arabia",
        "raw_text": "MEDITERRANEAN SHIPPING COMPANY\nBILL OF LADING\n\nB/L NO: MSC-DAM-2024-7789\n\nSHIPPER:\nSABIC TRADING COMPANY\nP.O. BOX 5101, RIYADH 11422\nKINGDOM OF SAUDI ARABIA\n\nCONSIGNEE:\nTO ORDER\n\nNOTIFY PARTY:\nTIANJIN BOHAI CHEMICAL IMPORT & EXPORT CO.,LTD.\nNO.88 DAGANG PETROCHEMICAL ROAD\nBINHAI NEW AREA, TIANJIN 300270, CHINA\n\nVESSEL: MSC RANIA\nVOYAGE: V.445E\n\nPORT OF LOADING: DAMMAM, SAUDI ARABIA\nPORT OF DISCHARGE: DALIAN, CHINA\nPLACE OF DELIVERY: DALIAN, CHINA\n\nDESCRIPTION OF GOODS:\n8,000 BAGS STC:\nLLDPE (LINEAR LOW DENSITY POLYETHYLENE)\nGRADE 218W\nPACKED IN 25KG BAGS\nTOTAL: 200 METRIC TONS\n\nGROSS WEIGHT: 200,000 KGS\nMEASUREMENT: 400 CBM\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: DAMMAM, AUGUST 23, 2024\n\nLOADED ON BOARD DATE: AUGUST 22, 2024\n\nSIGNED BY:\n____________________\nMSC AGENCY SAUDI ARABIA\n\nCLEAN ON BOARD"
      },
      "insurance_policy": {
        "policy_number": "TAWUNIYA-2024-22345",
        "insured": "SABIC Trading Company",
        "insurance_amount": 495000.00,
        "currency": "USD",
        "coverage": "All Risks",
        "goods_description": "200 Metric Tons of LLDPE",
        "vessel": "MSC Rania",
        "from": "Dammam, Saudi Arabia",
        "to": "Tianjin, China",
        "issue_date": "2024-08-21",
        "claims_payable_at": "Tianjin, China",
        "raw_text": "TAWUNIYA\nINSURANCE COMPANY\n\nMARINE CARGO INSURANCE POLICY\n\nPOLICY NO: TAWUNIYA-2024-22345\n\nTHE INSURED: SABIC TRADING COMPANY\nRIYADH, SAUDI ARABIA\n\nVOYAGE: FROM DAMMAM, SAUDI ARABIA TO TIANJIN, CHINA\nPER S.S.: MSC RANIA V.445E\n\nSUM INSURED: USD495,000.00\n(U.S.DOLLARS FOUR HUNDRED NINETY-FIVE THOUSAND ONLY)\n\nDESCRIPTION OF GOODS:\n200 METRIC TONS OF LLDPE\n(LINEAR LOW DENSITY POLYETHYLENE)\n\nPREMIUM: AS ARRANGED\nDATE OF ISSUE: AUGUST 21, 2024\n\nCONDITIONS: ALL RISKS\n(WAR RISKS NOT INCLUDED)\n\nCLAIMS PAYABLE AT: TIANJIN, CHINA\n\nFOR TAWUNIYA INSURANCE CO.\n\nAUTHORIZED SIGNATURE\n\nTHIS POLICY IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-09-05",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Commercial Invoice",
            "field": "invoice_amount",
            "description": "发票金额USD 460,000超过信用证金额USD 450,000，且L/C规定零容差（+/- 0%）",
            "ucp_reference": "UCP600 Article 18(b) - 发票金额不得超过信用证金额",
            "severity": "严重"
          },
          {
            "document": "Commercial Invoice",
            "field": "unit_price",
            "description": "发票单价USD 2,300/MT与信用证隐含单价USD 2,250/MT不符（450,000/200）",
            "ucp_reference": "UCP600 Article 18(a) - 发票必须看似由受益人出具，并以申请人为抬头",
            "severity": "一般"
          },
          {
            "document": "Bill of Lading",
            "field": "onboard_date",
            "description": "提单装船日期2024年8月22日晚于信用证最迟装运日2024年8月20日",
            "ucp_reference": "UCP600 Article 20(c) - 提单日期必须在信用证规定的装运期限内",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "port_of_discharge",
            "description": "提单显示卸货港为大连，信用证要求天津",
            "ucp_reference": "UCP600 Article 20(a)(iii) - 提单必须显示信用证规定的卸货港",
            "severity": "严重"
          },
          {
            "document": "Insurance Policy",
            "field": "coverage",
            "description": "保险单仅承保All Risks，缺少信用证要求的War Risks（战争险）",
            "ucp_reference": "UCP600 Article 28(a) - 保险单必须承保信用证要求的险别",
            "severity": "严重"
          },
          {
            "document": "Insurance Policy",
            "field": "insurance_amount",
            "description": "保险金额USD 495,000为发票金额的107.6%，未达到信用证要求的110%（应为USD 506,000）",
            "ucp_reference": "UCP600 Article 28(f)(ii) - 保险金额必须至少为发票金额的110%",
            "severity": "严重"
          }
        ],
        "overall_assessment": "存在多项严重不符点：发票超额、迟装运、港口错误、保险不足且缺战争险。建议拒付。"
      }
    },
    {
      "case_id": "case_09",
      "case_description": "细微不符点案例（木材：加拿大松木）",
      "letter_of_credit": {
        "lc_number": "LC2024-CA-223",
        "issuing_bank": "中国光大银行青岛分行",
        "advising_bank": "加拿大皇家银行温哥华分行",
        "applicant": {
          "name": "青岛良木家具制造有限公司",
          "address": "青岛市即墨区蓝村镇木材市场8号"
        },
        "beneficiary": {
          "name": "West Coast Lumber Trading Inc.",
          "address": "1250 West Georgia Street, Vancouver, BC V6E 4T1, Canada"
        },
        "currency": "USD",
        "amount": 186000.00,
        "amount_tolerance": "+/- 5%",
        "goods_description": "300 Cubic Meters of Canadian SPF (Spruce-Pine-Fir) Lumber, KD 19%, Grade #2&BTR, 2x4x8', packed in bulk",
        "latest_shipment_date": "2024-09-15",
        "expiry_date": "2024-10-06",
        "expiry_place": "Vancouver, Canada",
        "presentation_period": "21 days after the date of shipment",
        "loading_port": "Vancouver, Canada",
        "discharge_port": "Qingdao, China",
        "trade_terms": "CIF Qingdao",
        "partial_shipment": "Allowed",
        "transhipment": "Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading made out to order, marked freight prepaid, notify applicant",
          "Insurance policy for 110% of CIF value covering All Risks",
          "Phytosanitary Certificate",
          "Certificate of Origin"
        ],
        "additional_conditions": [
          "Beneficiary name must exactly match L/C",
          "Quantity unit must be clearly stated"
        ],
        "raw_text": "IRREVOCABLE DOCUMENTARY CREDIT\nNO.: LC2024-CA-223\nISSUING BANK: CHINA EVERBRIGHT BANK QINGDAO BRANCH\nADVISING BANK: ROYAL BANK OF CANADA VANCOUVER BRANCH\nAPPLICANT:\nQINGDAO LIANGMU FURNITURE MANUFACTURING CO.,LTD.\nNO.8 LUMBER MARKET, LANCM TOWN\nJIMO DISTRICT, QINGDAO 266200, CHINA\nBENEFICIARY:\nWEST COAST LUMBER TRADING INC.\n1250 WEST GEORGIA STREET\nVANCOUVER, BC V6E 4T1, CANADA\nAMOUNT: USD186,000.00 (+/-5%)\nEXPIRY DATE: OCTOBER 6, 2024\nPLACE: VANCOUVER, CANADA\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: ALLOWED\nTRANSSHIPMENT: ALLOWED\nLOADING: VANCOUVER, CANADA\nDESTINATION: QINGDAO, CHINA\nLATEST SHIPMENT: SEPTEMBER 15, 2024\nTRADE TERMS: CIF QINGDAO\nGOODS:\n300 CUBIC METERS OF CANADIAN SPF (SPRUCE-PINE-FIR) LUMBER\nKD 19%, GRADE #2&BTR, 2X4X8'\nPACKED IN BULK\nDOCUMENTS REQUIRED:\n-SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n-FULL SET CLEAN ON BOARD B/L TO ORDER\n-FREIGHT PREPAID, NOTIFY APPLICANT\n-INSURANCE POLICY 110% OF CIF COVERING ALL RISKS\n-PHYTOSANITARY CERTIFICATE\n-CERTIFICATE OF ORIGIN\nCONDITIONS:\nBENEFICIARY NAME MUST EXACTLY MATCH L/C\nQUANTITY UNIT MUST BE CLEARLY STATED\nPRESENTATION: 21 DAYS AFTER SHIPMENT\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "WCL-2024-QD-112",
        "invoice_date": "2024-09-12",
        "issued_by": "West Coast Lumber Trading Inc.",
        "issued_to": "青岛良木家具制造有限公司",
        "currency": "USD",
        "goods": [
          {
            "description": "300 CBM of Canadian SPF (Spruce-Pine-Fir) Lumber, KD 19%, Grade #2&BTR, 2x4x8', packed in bulk",
            "quantity": 300,
            "unit": "CBM",
            "unit_price": 620.00,
            "amount": 186000.00
          }
        ],
        "total_amount": 186000.00,
        "trade_terms": "CIF Qingdao",
        "raw_text": "WEST COAST LUMBER TRADING INC.\n1250 WEST GEORGIA STREET\nVANCOUVER, BC V6E 4T1, CANADA\nTEL: +1-604-123-4567\n\nCOMMERCIAL INVOICE\n\nInvoice No: WCL-2024-QD-112\nDate: Sept. 12, 2024\nL/C No: LC2024-CA-223\n\nSold to:\nQINGDAO LIANGMU FURNITURE MFG. CO.,LTD.\nNO.8 LUMBER MARKET, LANCM TOWN\nJIMO DIST., QINGDAO 266200, CHINA\n\nVessel: OOCL California V.228W\nFrom Vancouver, Canada to Qingdao, China\n\nDescription:\n300 CBM Canadian SPF (Spruce-Pine-Fir) Lumber\nKD 19%, Grade #2&BTR, 2x4x8'\nin bulk\n\nQuantity: 300 CBM\nUnit Price: USD620.00/CBM\nTotal: USD186,000.00\n\nSAY US DOLLARS ONE HUNDRED EIGHTY-SIX THOUSAND ONLY\n\nTerms: CIF Qingdao\nOrigin: British Columbia, Canada\n\nAuthorized Signature:\nJohn MacDonald\nVP Sales\n\nBank: RBC Royal Bank\nTransit: 00012\nA/C: 1234567\nSWIFT: ROYCCAT2"
      },
      "bill_of_lading": {
        "bl_number": "OOCU-VAN-2024-4456",
        "shipper": "West Coast Lumber Trading Incorporated, Vancouver, Canada",
        "consignee": "To Order",
        "notify_party": "青岛良木家具制造有限公司, 青岛市即墨区蓝村镇木材市场8号",
        "vessel": "OOCL California",
        "voyage": "V.228W",
        "port_of_loading": "Vancouver, BC, Canada",
        "port_of_discharge": "Qingdao, China",
        "onboard_date": "2024-09-14",
        "issue_date": "2024-09-15",
        "goods_description": "300 cubic meters Canadian SPF Lumber, KD 19%, Grade #2 and Better, 2 by 4 by 8 feet, in bulk",
        "number_of_packages": "In Bulk",
        "gross_weight": "135 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "OOCL Canada Inc.",
        "raw_text": "ORIENT OVERSEAS CONTAINER LINE\nBILL OF LADING\n\nB/L NO: OOCU-VAN-2024-4456\n\nSHIPPER:\nWEST COAST LUMBER TRADING INCORPORATED\n1250 WEST GEORGIA STREET\nVANCOUVER, BC V6E 4T1, CANADA\n\nCONSIGNEE:\nTO ORDER\n\nNOTIFY PARTY:\nQINGDAO LIANGMU FURNITURE MANUFACTURING CO.,LTD.\nNO.8 LUMBER MARKET, LANCM TOWN\nJIMO DISTRICT, QINGDAO 266200, CHINA\n\nVESSEL: OOCL CALIFORNIA\nVOYAGE: V.228W\n\nPORT OF LOADING: VANCOUVER, BC, CANADA\nPORT OF DISCHARGE: QINGDAO, CHINA\n\nDESCRIPTION OF GOODS:\n300 CUBIC METERS CANADIAN SPF LUMBER\n(SPRUCE-PINE-FIR)\nKD 19%, GRADE #2 AND BETTER\n2 BY 4 BY 8 FEET, IN BULK\n\nGROSS WEIGHT: 135,000 KGS (135 MT)\nMEASUREMENT: 300 CBM\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: VANCOUVER, SEPTEMBER 15, 2024\n\nLOADED ON BOARD DATE: SEPTEMBER 14, 2024\n\nSIGNED BY:\n_________________\nOOCL CANADA INC.\n\nCLEAN ON BOARD"
      },
      "insurance_policy": {
        "policy_number": "INTACT-CA-2024-8834",
        "insured": "West Coast Lumber Trading Inc.",
        "insurance_amount": 204600.00,
        "currency": "USD",
        "coverage": "All Risks",
        "goods_description": "300 Cubic Meters of Canadian SPF Lumber",
        "vessel": "OOCL California",
        "from": "Vancouver, Canada",
        "to": "Qingdao, China",
        "issue_date": "2024-09-13",
        "claims_payable_at": "Qingdao, China",
        "raw_text": "INTACT INSURANCE COMPANY\nMARINE CARGO INSURANCE CERTIFICATE\n\nCERTIFICATE NO: INTACT-CA-2024-8834\n\nNAMED INSURED: WEST COAST LUMBER TRADING INC.\nVANCOUVER, BC, CANADA\n\nVOYAGE: FROM VANCOUVER, CANADA TO QINGDAO, CHINA\nVESSEL: OOCL CALIFORNIA V.228W\n\nINSURED VALUE: USD204,600.00\n(U.S.DOLLARS TWO HUNDRED FOUR THOUSAND SIX HUNDRED ONLY)\n\nINTEREST INSURED:\n300 CUBIC METERS OF CANADIAN SPF LUMBER\n\nCONDITIONS: ALL RISKS\n\nDATE OF ISSUE: SEPTEMBER 13, 2024\nCLAIMS PAYABLE AT: QINGDAO, CHINA\n\nFOR INTACT INSURANCE:\n\nAUTHORIZED SIGNATURE\n\nTHIS CERTIFICATE IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-09-30",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Commercial Invoice",
            "field": "beneficiary_name",
            "description": "发票显示受益人名称为'West Coast Lumber Trading Inc.'，而信用证显示为'West Coast Lumber Trading Inc.'，但提单显示为'West Coast Lumber Trading Incorporated'（全称拼写），虽然实质相同但严格来说不一致",
            "ucp_reference": "UCP600 Article 18(a) - 发票必须由受益人出具，名称须严格一致",
            "severity": "轻微"
          },
          {
            "document": "Commercial Invoice",
            "field": "quantity_unit",
            "description": "信用证数量单位为'Cubic Meters'，发票缩写为'CBM'，虽行业通用但严格不符ISBP对缩写的规定",
            "ucp_reference": "ISBP 745 Paragraph A7 - 单据中应使用全称而非缩写，除非信用证允许",
            "severity": "轻微"
          },
          {
            "document": "Bill of Lading",
            "field": "shipper_name",
            "description": "提单托运人显示'West Coast Lumber Trading Incorporated'，而信用证受益人为'West Coast Lumber Trading Inc.'，'Inc.'与'Incorporated'严格来说不一致",
            "ucp_reference": "UCP600 Article 14(k) - 单据中受益人地址无需与L/C相同，但必须同国；名称应一致",
            "severity": "轻微"
          },
          {
            "document": "Multiple Documents",
            "field": "quantity_unit_variation",
            "description": "发票使用'CBM'，提单使用'cubic meters'，大小写及缩写不一致，虽含义相同但形式不统一",
            "ucp_reference": "UCP600 Article 14(d) - 单据之间不得互相矛盾，术语应一致",
            "severity": "轻微"
          }
        ],
        "overall_assessment": "存在多处细微不符点，主要为缩写与全称、大小写不一致，属于轻微不符点。在实务中银行可能联系申请人接受不符点，或根据银行内部政策决定。"
      }
    },
    {
      "case_id": "case_10",
      "case_description": "复杂综合案例（精密仪器：日本光学设备）",
      "letter_of_credit": {
        "lc_number": "LC2024-JP-990",
        "issuing_bank": "兴业银行武汉分行",
        "advising_bank": "三菱日联银行东京分行",
        "applicant": {
          "name": "武汉光谷精密仪器研究院",
          "address": "武汉市东湖新技术开发区光谷大道77号"
        },
        "beneficiary": {
          "name": "Nikon Precision Equipment Inc.",
          "address": "201-9 Mizugahara, Kumagaya, Saitama 360-0848, Japan"
        },
        "currency": "JPY",
        "amount": 48500000.00,
        "amount_tolerance": "+/- 0%",
        "goods_description": "1 Unit Step-and-Repeat System Model NSR-S635E, 300mm wafer compatible, ArF immersion lithography system, including installation and training",
        "latest_shipment_date": "2024-10-25",
        "expiry_date": "2024-11-15",
        "expiry_place": "Tokyo, Japan",
        "presentation_period": "15 days after the date of shipment but within the validity of this credit",
        "loading_port": "Yokohama, Japan",
        "discharge_port": "Shanghai, China",
        "trade_terms": "CIF Shanghai",
        "partial_shipment": "Not Allowed",
        "transhipment": "Not Allowed",
        "required_documents": [
          "Signed Commercial Invoice in 3 originals",
          "Full set of clean on board ocean bills of lading made out to order of issuing bank, marked freight prepaid, notify applicant",
          "Insurance policy for 110% of CIF value covering All Risks, War Risks and SRCC",
          "Packing List in 3 originals",
          "Certificate of Origin issued by Japan Chamber of Commerce",
          "Installation Certificate"
        ],
        "additional_conditions": [
          "Shipment must be effected on or before Oct 25, 2024",
          "Insurance must cover Institute Cargo Clauses (A)",
          "All documents must be in English"
        ],
        "raw_text": "IRREVOCABLE DOCUMENTARY CREDIT\nNUMBER: LC2024-JP-990\nISSUING BANK: INDUSTRIAL BANK CO.,LTD. WUHAN BRANCH\nADVISING BANK: MUFG BANK, LTD. TOKYO BRANCH\nAPPLICANT:\nWUHAN OPTICS VALLEY PRECISION INSTRUMENT RESEARCH INSTITUTE\nNO.77 GUANGGU AVENUE, DONGHU NEW TECHNOLOGY DEVELOPMENT ZONE\nWUHAN 430000, CHINA\nBENEFICIARY:\nNIKON PRECISION EQUIPMENT INC.\n201-9 MIZUGAHARA, KUMAGAYA\nSAITAMA 360-0848, JAPAN\nAMOUNT: JPY48,500,000.00 (ZERO TOLERANCE)\nEXPIRY DATE: NOVEMBER 15, 2024\nPLACE: TOKYO, JAPAN\nAVAILABLE: BY NEGOTIATION\nDRAFTS AT: SIGHT\nPARTIAL SHIPMENT: NOT ALLOWED\nTRANSSHIPMENT: NOT ALLOWED\nLOADING: YOKOHAMA, JAPAN\nDESTINATION: SHANGHAI, CHINA\nLATEST SHIPMENT: OCTOBER 25, 2024\nTRADE TERMS: CIF SHANGHAI\nGOODS:\n1 UNIT STEP-AND-REPEAT SYSTEM MODEL NSR-S635E\n300MM WAFER COMPATIBLE, ARF IMMERSION LITHOGRAPHY SYSTEM\nINCLUDING INSTALLATION AND TRAINING\nDOCUMENTS REQUIRED:\n1. SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS\n2. FULL SET CLEAN ON BOARD B/L MADE OUT TO ORDER OF ISSUING BANK\n   FREIGHT PREPAID, NOTIFY APPLICANT\n3. INSURANCE POLICY 110% OF CIF COVERING ALL RISKS, WAR RISKS AND SRCC\n4. PACKING LIST IN 3 ORIGINALS\n5. CERTIFICATE OF ORIGIN ISSUED BY JAPAN CHAMBER OF COMMERCE\n6. INSTALLATION CERTIFICATE\nCONDITIONS:\nSHIPMENT MUST BE EFFECTED ON OR BEFORE OCT 25, 2024\nINSURANCE MUST COVER INSTITUTE CARGO CLAUSES (A)\nALL DOCUMENTS MUST BE IN ENGLISH\nPRESENTATION: 15 DAYS AFTER SHIPMENT\nSUBJECT TO UCP600"
      },
      "commercial_invoice": {
        "invoice_number": "NPE-2024-WH-667",
        "invoice_date": "2024-10-22",
        "issued_by": "Nikon Precision Equipment Inc.",
        "issued_to": "武汉光谷精密仪器研究院",
        "currency": "JPY",
        "goods": [
          {
            "description": "1 Unit Step-and-Repeat System Model NSR-S635E, 300mm wafer compatible, ArF immersion lithography system, including installation",
            "quantity": 1,
            "unit": "Unit",
            "unit_price": 48500000.00,
            "amount": 48500000.00
          }
        ],
        "total_amount": 48500000.00,
        "trade_terms": "CIF Shanghai",
        "raw_text": "NIKON PRECISION EQUIPMENT INC.\n201-9 MIZUGAHARA, KUMAGAYA\nSAITAMA 360-0848, JAPAN\nTEL: +81-48-123-4567\n\nCOMMERCIAL INVOICE\n\nInvoice No: NPE-2024-WH-667\nDate: October 22, 2024\nL/C No: LC2024-JP-990\n\nSold to:\nWUHAN OPTICS VALLEY PRECISION INSTRUMENT RESEARCH INSTITUTE\nNO.77 GUANGGU AVENUE\nDONGHU NEW TECHNOLOGY DEVELOPMENT ZONE\nWUHAN 430000, CHINA\n\nShipped per: NYK Aquarius V.445E\nFrom Yokohama, Japan to Shanghai, China\n\nDescription of Goods:\n1 Unit Step-and-Repeat System\nModel: NSR-S635E\n300mm wafer compatible\nArF immersion lithography system\nincluding installation\n\nQuantity: 1 Unit\nUnit Price: JPY48,500,000.00\nTotal Amount: JPY48,500,000.00\n\nSAY JAPANESE YEN FORTY-EIGHT MILLION FIVE HUNDRED THOUSAND ONLY\n\nTerms: CIF Shanghai\nOrigin: Japan\n\nNote: Training to be provided at buyer's site within 30 days of installation.\n\nAuthorized Signature:\nTakeshi Yamamoto\nGeneral Manager\nInternational Sales Division\n\nBank: MUFG Bank, Ltd.\nBranch: Kumagaya\nA/C: 1234567\nSWIFT: BOTKJPJT"
      },
      "bill_of_lading": {
        "bl_number": "NYK-YOK-2024-2234",
        "shipper": "Nikon Precision Equipment Inc., Saitama, Japan",
        "consignee": "To Order of Industrial Bank Wuhan Branch",
        "notify_party": "武汉光谷精密仪器研究院, 武汉市东湖新技术开发区光谷大道77号",
        "vessel": "NYK Aquarius",
        "voyage": "V.445E",
        "port_of_loading": "Nagoya, Japan",
        "port_of_discharge": "Shanghai, China",
        "onboard_date": "2024-10-28",
        "issue_date": "2024-10-29",
        "goods_description": "1 Unit Precision Optical Equipment, Model NSR-S635E, packed in 3 wooden cases and 1 crate",
        "number_of_packages": "4 packages",
        "gross_weight": "45 MT",
        "freight": "Freight Prepaid",
        "number_of_originals": "3/3",
        "clean_onboard": true,
        "carrier_signature": "Nippon Yusen Kaisha, Yokohama",
        "raw_text": "NIPPON YUSEN KAISHA\nBILL OF LADING\n\nB/L NO: NYK-YOK-2024-2234\n\nSHIPPER:\nNIKON PRECISION EQUIPMENT INC.\n201-9 MIZUGAHARA, KUMAGAYA\nSAITAMA 360-0848, JAPAN\nCONTACT: MR. TAKESHI YAMAMOTO\nTEL: +81-48-123-4567\n\nCONSIGNEE:\nTO ORDER OF INDUSTRIAL BANK WUHAN BRANCH\n\nNOTIFY PARTY:\nWUHAN OPTICS VALLEY PRECISION INSTRUMENT RESEARCH INSTITUTE\nNO.77 GUANGGU AVENUE\nDONGHU NEW TECHNOLOGY DEVELOPMENT ZONE\nWUHAN 430000, CHINA\nTEL: +86-27-1234-5678\n\nPRE-CARRIAGE BY: TRUCK\nPLACE OF RECEIPT: SAITAMA, JAPAN\n\nOCEAN VESSEL: NYK AQUARIUS\nVOYAGE NO.: V.445E\nPORT OF LOADING: NAGOYA, JAPAN\nPORT OF DISCHARGE: SHANGHAI, CHINA\nPLACE OF DELIVERY: SHANGHAI, CHINA\n\nCONTAINER NO: NYKU1234567\nSEAL: JP123456\n\nDESCRIPTION OF PACKAGES:\n4 PACKAGES STC:\n1 UNIT PRECISION OPTICAL EQUIPMENT\nMODEL NSR-S635E\nPACKED IN 3 WOODEN CASES AND 1 CRATE\nDIMENSIONS: 12.5 x 3.2 x 3.0 M\nGROSS WEIGHT: 45,000 KGS (45 MT)\n\n*** TRANSSHIPMENT AT BUSAN, KOREA ***\n\nFREIGHT: PREPAID\nNUMBER OF ORIGINALS: THREE(3)\n\nPLACE AND DATE OF ISSUE: YOKOHAMA, OCTOBER 29, 2024\n\nLOADED ON BOARD DATE: OCTOBER 28, 2024\n\nSIGNED BY:\n_____________________\nNIPPON YUSEN KAISHA\nYOKOHAMA AGENT\n\nCLEAN ON BOARD\nSHIPPED IN APPARENT GOOD ORDER AND CONDITION"
      },
      "insurance_policy": {
        "policy_number": "TOKIO-JP-2024-77891",
        "insured": "Nikon Precision Equipment Inc.",
        "insurance_amount": 48000000.00,
        "currency": "JPY",
        "coverage": "All Risks and War Risks",
        "goods_description": "1 Unit Step-and-Repeat System Model NSR-S635E",
        "vessel": "NYK Aquarius",
        "from": "Yokohama, Japan",
        "to": "Shanghai, China",
        "issue_date": "2024-10-27",
        "claims_payable_at": "Shanghai, China",
        "raw_text": "TOKIO MARINE & NICHIDO FIRE INSURANCE CO., LTD.\nMARINE CARGO INSURANCE POLICY\n\nPOLICY NO: TOKIO-JP-2024-77891\n\nTHE INSURED: NIKON PRECISION EQUIPMENT INC.\nKUMAGAYA, SAITAMA, JAPAN\n\nVOYAGE: FROM YOKOHAMA, JAPAN TO SHANGHAI, CHINA\nPER S.S.: NYK AQUARIUS V.445E\n\nSUM INSURED: JPY48,000,000.00\n(JAPANESE YEN FORTY-EIGHT MILLION ONLY)\n\nDESCRIPTION OF GOODS:\n1 UNIT STEP-AND-REPEAT SYSTEM MODEL NSR-S635E\n\nPREMIUM: AS ARRANGED\nDATE OF ISSUE: OCTOBER 27, 2024\n\nCONDITIONS: ALL RISKS AND WAR RISKS\n(SRCC NOT INCLUDED)\n\nCLAIMS PAYABLE AT: SHANGHAI, CHINA\n\nFOR TOKIO MARINE & NICHIDO FIRE INSURANCE CO., LTD.\n\nAUTHORIZED SIGNATURE\n\nTHIS POLICY IS ISSUED IN DUPLICATE"
      },
      "presentation_date": "2024-11-12",
      "expected_result": {
        "has_discrepancies": true,
        "discrepancies": [
          {
            "document": "Commercial Invoice",
            "field": "goods_description",
            "description": "发票货物描述中删除了'training'（培训），与信用证要求的'description including installation and training'不符",
            "ucp_reference": "UCP600 Article 18(c) - 发票中的货物描述必须与信用证相符",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "port_of_loading",
            "description": "提单显示装货港为名古屋（Nagoya），信用证要求为横滨（Yokohama），港口不一致",
            "ucp_reference": "UCP600 Article 20(a)(iii) - 提单必须显示信用证规定的装货港",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "onboard_date",
            "description": "提单装船日期为2024年10月28日，晚于信用证最迟装运日2024年10月25日",
            "ucp_reference": "UCP600 Article 20(c) - 提单日期必须在信用证规定的装运期限内",
            "severity": "严重"
          },
          {
            "document": "Bill of Lading",
            "field": "transhipment_indicator",
            "description": "提单显示在釜山（Busan）转运，而信用证规定'Transhipment: Not Allowed'（不允许转运）",
            "ucp_reference": "UCP600 Article 20(c) - 提单不得表明货物将要或已经被转运",
            "severity": "严重"
          },
          {
            "document": "Insurance Policy",
            "field": "insurance_amount",
            "description": "保险金额JPY 48,000,000仅为发票金额的98.9%，未达到信用证要求的110%（应为JPY 53,350,000）",
            "ucp_reference": "UCP600 Article 28(f)(ii) - 保险金额必须至少为发票金额的110%",
            "severity": "严重"
          },
          {
            "document": "Insurance Policy",
            "field": "coverage",
            "description": "保险单缺少信用证要求的SRCC（Strikes, Riots and Civil Commotions，罢工、暴动和民变险）",
            "ucp_reference": "UCP600 Article 28(a) - 保险单必须承保信用证要求的险别",
            "severity": "一般"
          },
          {
            "document": "Insurance Policy",
            "field": "loading_port",
            "description": "保险单显示起运地为横滨（与信用证一致），但提单显示名古屋，保险单与运输单据不一致",
            "ucp_reference": "UCP600 Article 28(h) - 保险单必须与运输单据相符",
            "severity": "一般"
          },
          {
            "document": "Presentation",
            "field": "presentation_date",
            "description": "交单日期2024年11月12日距离提单日期2024年10月28日已15天，虽在15天内，但已超过信用证有效期（2024年11月15日）前合理时间，且接近截止日",
            "ucp_reference": "UCP600 Article 14(c) - 单据必须在信用证有效期内提交",
            "severity": "一般"
          }
        ],
        "overall_assessment": "存在多项严重不符点：货描缺失、装货港错误、迟装运、违规转运、保险严重不足，构成复杂综合不符点案例。建议拒付。"
      }
    }
  ],
  "metadata": {
    "total_cases": 10,
    "compliant_cases": 2,
    "discrepancy_cases": 8,
    "discrepancy_distribution": {
      "commercial_invoice_only": 1,
      "bill_of_lading_only": 1,
      "insurance_only": 1,
      "presentation_only": 1,
      "inter_document_conflict": 1,
      "multiple_documents": 2,
      "minor_discrepancies": 1,
      "complex_comprehensive": 1
    },
    "ucp_articles_covered": [
      "Article 6(d)(i)",
      "Article 14(c)",
      "Article 14(d)",
      "Article 14(k)",
      "Article 18(a)",
      "Article 18(b)",
      "Article 18(c)",
      "Article 20(a)(iii)",
      "Article 20(c)",
      "Article 27(a)",
      "Article 28(a)",
      "Article 28(e)",
      "Article 28(f)(ii)",
      "Article 28(h)",
      "Article 30(b)"
    ],
    "industries_covered": [
      "Agricultural Products",
      "Machinery Equipment",
      "Chemical Products",
      "Textiles",
      "Electronics",
      "Minerals",
      "Wood Products",
      "Precision Instruments"
    ],
    "currencies_used": ["USD", "EUR", "JPY"],
    "ocr_features_simulated": [
      "Irregular line breaks",
      "Mixed case text",
      "Tabular data with ASCII characters",
      "Handwritten signature placeholders",
      "Inconsistent spacing",
      "Mixed Chinese and English text",
      "SWIFT message format",
      "Standard commercial document formats"
    ]
  }
}