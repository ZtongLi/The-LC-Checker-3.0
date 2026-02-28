{
  "document_title": "信用证智能审单系统测试数据集",
  "version": "1.0",
  "generated_date": "2024-02-27",
  "description": "基于UCP600和ISBP745标准的10组信用证审单测试数据，用于AI审单系统准确性测试",
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
        ]
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
        "trade_terms": "CIF Shenzhen"
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
        "carrier_signature": "MSC Mediterranean Shipping Company, Santos Agent"
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
        "claims_payable_at": "Shenzhen, China"
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
        ]
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
        "trade_terms": "CIF Qingdao"
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
        "carrier_signature": "Hapag-Lloyd AG, Hamburg"
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
        "claims_payable_at": "Qingdao, China"
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
        ]
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
        "trade_terms": "CIF Ningbo"
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
        "carrier_signature": "Ocean Network Express Pte. Ltd."
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
        "claims_payable_at": "Ningbo, China"
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
        ]
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
        "trade_terms": "FOB Ho Chi Minh City"
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
        "carrier_signature": "HMM Co., Ltd., Ho Chi Minh Agent"
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
        "claims_payable_at": "Guangzhou, China"
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
        ]
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
        "trade_terms": "CIF Shanghai"
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
        "carrier_signature": "China Airlines Cargo"
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
        "claims_payable_at": "Taipei, Taiwan"
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
        ]
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
        "trade_terms": "CIF Xiamen"
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
        "carrier_signature": "RCL Agencies (Thailand) Ltd."
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
        "claims_payable_at": "Xiamen, China"
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
        "advising银行": "澳大利亚联邦银行珀斯分行",
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
        ]
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
        "trade_terms": "CFR Tangshan"
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
        "carrier_signature": "Fortescue Metals Group, Port Hedland"
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
        "claims_payable_at": "Tangshan, China"
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
        "advising银行": "利雅得银行达曼分行",
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
        ]
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
        "trade_terms": "CIF Tianjin"
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
        "carrier_signature": "MSC Agency Saudi Arabia"
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
        "claims_payable_at": "Tianjin, China"
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
        "advising银行": "加拿大皇家银行温哥华分行",
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
        ]
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
        "trade_terms": "CIF Qingdao"
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
        "carrier_signature": "OOCL Canada Inc."
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
        "claims_payable_at": "Qingdao, China"
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
        "advising银行": "三菱日联银行东京分行",
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
        ]
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
        "trade_terms": "CIF Shanghai"
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
        "carrier_signature": "Nippon Yusen Kaisha, Yokohama"
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
        "claims_payable_at": "Shanghai, China"
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
    "currencies_used": ["USD", "EUR", "JPY"]
  }
}