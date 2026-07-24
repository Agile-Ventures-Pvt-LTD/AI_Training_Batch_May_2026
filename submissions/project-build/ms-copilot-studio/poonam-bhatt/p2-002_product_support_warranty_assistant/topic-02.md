kind: AdaptiveDialog
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent:
    triggerQueries:
      - tell me about topic 02
      - what is topic 02
      - explain topic-02
      - give details on topic two
      - information on topic-02
      - topic two overview
      - describe topic-02
      - learn about topic two
      - topic-02 details

  actions:
    - kind: Question
      id: Question_Sv4pFB
      variable: Topic.ProductFamily
      prompt: What is the product family?
      entity:
        kind: EmbeddedEntity
        definition:
          kind: ClosedListEntity
          optionSetName: ProductFamilyOptions
          items:
            - id: laptop
              displayName: Laptop

            - id: printer
              displayName: Printer

    - kind: Question
      id: Question_x0KLSt
      variable: Topic.ProductModel
      prompt: What is the product model?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_7iYO7p
      variable: Topic.ItemCategory
      prompt: What is the item category?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_Uh7p0H
      variable: Topic.PurchaseDate
      prompt: What is the purchase date?
      entity: DatePrebuiltEntity

    - kind: Question
      id: Question_RwpCB9
      variable: Topic.DeliveryDate
      prompt: What is the delivery date? (optional)
      entity: DatePrebuiltEntity

    - kind: Question
      id: Question_aIXk9m
      variable: Topic.PurchasedFromNovaRetail
      prompt: Was the product purchased from NovaRetail?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_xnl7SM
      variable: Topic.InvoiceAvailable
      prompt: Is the invoice available?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_L30Upy
      variable: Topic.SerialNumberAvailable
      prompt: Is the serial number available?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_otsYYI
      variable: Topic.IssueCategory
      prompt: What is the issue category?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_6n5wXT
      variable: Topic.ProductStillWorks
      prompt: Does the product still work?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_VvzKuJ
      variable: Topic.AccidentalDamage
      prompt: Is there accidental damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_WXjvbT
      variable: Topic.LiquidExposure
      prompt: Has the product been exposed to liquid?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_DWPvd6
      variable: Topic.ElectricalSurge
      prompt: Was there an electrical surge?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_R6G1XR
      variable: Topic.UnauthorizedRepair
      prompt: Has the product been repaired or modified by an unauthorized service center?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_RBuOnV
      variable: Topic.ConsumableItem
      prompt: Is the item a consumable such as toner or paper?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_qAPSlg
      variable: Topic.ReportedWithinSevenDays
      prompt: Was the issue reported within seven days of delivery?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_WAIq8S
      variable: Topic.TroubleshootingCompleted
      prompt: Has troubleshooting already been completed?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_O2SYVC
      variable: Topic.PreviousRepairs
      prompt: How many previous repairs have been performed?
      entity: NumberPrebuiltEntity

    - kind: Question
      id: Question_2LK8fa
      variable: Topic.DisagreeWithAssessment
      prompt: Do you disagree with the preliminary assessment?
      entity: BooleanPrebuiltEntity

    - kind: SendActivity
      id: SendActivity_NeXi3t
      activity: Thank you. Your warranty information has been collected and will be used for the warranty assessment.

    - kind: ConditionGroup
      id: ConditionGroup_30KkVB
      conditions:
        - id: ConditionItem_Btfiiy
          condition: =Topic.ProductFamily = ProductFamilyOptions.laptop
          actions:
            - kind: ConditionGroup
              id: ConditionGroup_LWrGkZ
              conditions:
                - id: ConditionItem_5S0ALa
                  condition: =Topic.ProductModel = "Lenovo ThinkPad E14 Gen 5"

              elseActions:
                - kind: SendActivity
                  id: SendActivity_qWApPJ
                  activity: Your laptop model is not supported for automated assessment. Only a general assessment can be provided. Your case will be routed to Human Review.

        - id: ConditionItem_YOA5vd
          condition: =Topic.ProductFamily = ProductFamilyOptions.printer
          actions:
            - kind: ConditionGroup
              id: ConditionGroup_xb1dGH
              conditions:
                - id: ConditionItem_YnkiYj
                  condition: =Topic.ProductModel = "HP LaserJet Pro MFP M428-M429"

              elseActions:
                - kind: SendActivity
                  id: SendActivity_M4nlkD
                  activity: Your printer model is not supported for automated assessment. Only a general assessment can be provided. Your case will be routed to Human Review.

    - kind: ConditionGroup
      id: ConditionGroup_J7vpZL
      conditions:
        - id: ConditionItem_0I8adU
          condition: =Topic.ItemCategory = "Laptop" || Topic.ItemCategory = "Printer"
          actions:
            - kind: SendActivity
              id: SendActivity_XWtBlh
              activity: "Your product is covered under standard warranty for 12 months. Classification: Within Coverage."

        - id: ConditionItem_iimXJT
          condition: =Topic.ItemCategory = "Bundled Laptop Battery" || Topic.ItemCategory = "Bundled Accessory"
          actions:
            - kind: SendActivity
              id: SendActivity_gjwnSJ
              activity: "Your item is covered under standard warranty for 6 months. Classification: Within Coverage."

        - id: ConditionItem_ZljlNN
          condition: =Topic.ItemCategory = "Printer Toner" || Topic.ItemCategory = "Printer Paper" || Topic.ItemCategory = "Other Consumables"
          actions:
            - kind: SendActivity
              id: SendActivity_yc2Hoi
              activity: "This item is not covered under standard warranty. Classification: Outside Standard Coverage."

      elseActions:
        - kind: SendActivity
          id: SendActivity_TwzTn8
          activity: "Unable to determine warranty coverage for the selected item category. Classification: Unable to Determine."

    - kind: ConditionGroup
      id: ConditionGroup_ptdaB2
      conditions:
        - id: ConditionItem_ZAMaMJ
          condition: =Topic.PurchasedFromNovaRetail = true && Topic.ReportedWithinSevenDays = true && Topic.ProductStillWorks = false && Topic.AccidentalDamage = false && Topic.LiquidExposure = false
          actions:
            - kind: SendActivity
              id: SendActivity_rPhBBx
              activity: This case may qualify for a Dead-on-Arrival assessment. A warranty specialist will perform the final review.

    - kind: ConditionGroup
      id: ConditionGroup_iJDrZY
      conditions:
        - id: ConditionItem_TP5nOM
          condition: =Topic.AccidentalDamage = true || Topic.LiquidExposure = true || Topic.ElectricalSurge = true || Topic.UnauthorizedRepair = true || Topic.UnauthorizedModification = true || Topic.ConsumableItem = true
          actions:
            - kind: SendActivity
              id: SendActivity_v4WiUg
              activity: Based on the information provided, this issue may fall under a warranty exclusion. A warranty specialist will review your case.

    - kind: ConditionGroup
      id: ConditionGroup_et624e
      conditions:
        - id: ConditionItem_A3kqo3
          condition: =Topic.PreviousRepairs > 0
          actions:
            - kind: SendActivity
              id: SendActivity_AYkvMN
              activity: This issue has been repaired previously and will be reviewed by our repeat repair team.

    - kind: ConditionGroup
      id: ConditionGroup_0psc34
      conditions:
        - id: ConditionItem_FAyVSd
          condition: =Topic.PurchasedFromNovaRetail = true && Topic.ReportedWithinSevenDays = true && Topic.AccidentalDamage = false && Topic.LiquidExposure = false && Topic.ProductStillWorks = false
          actions:
            - kind: SendActivity
              id: SendActivity_FAhPlt
              activity: This case may qualify for a Dead-on-Arrival assessment. A warranty specialist will review your request.

    - kind: ConditionGroup
      id: ConditionGroup_LuWHUC
      conditions:
        - id: ConditionItem_sAYXVA
          condition: =Topic.AccidentalDamage = true || Topic.LiquidExposure = true || Topic.ElectricalSurge = true || Topic.UnauthorizedRepair = true || Topic.UnauthorizedModification = true || Topic.ConsumableItem = true
          actions:
            - kind: SendActivity
              id: SendActivity_AHiw5e
              activity: Based on the information provided, this issue may fall under a warranty exclusion. A warranty specialist will review your case.

    - kind: Question
      id: Question_pllvfL
      variable: Topic.WarrantySummaryConfirmed
      prompt: Is this information correct?
      entity: BooleanPrebuiltEntity

    - kind: SendActivity
      id: SendActivity_jXidz0
      activity:
        attachments:
          - kind: AdaptiveCardTemplate
            cardContent: "={ type: \"AdaptiveCard\", body: [ { type: \"TextBlock\", size: \"Medium\", weight: \"Bolder\", text: \"Warranty Summary\" }, { type: \"FactSet\", facts: [ { title: \"Product Family\", value: Text(Topic.ProductFamily) }, { title: \"Product Model\", value: Text(Topic.ProductModel) }, { title: \"Item Category\", value: Text(Topic.ItemCategory) }, { title: \"Purchase Date\", value: Text(Topic.PurchaseDate) }, { title: \"Issue Category\", value: Text(Topic.IssueCategory) }, { title: \"Damage Information\", value: Text(Topic.AccidentalDamage) + \", \" + Text(Topic.LiquidExposure) + \", \" + Text(Topic.ElectricalSurge) }, { title: \"Warranty Classification\", value: Text(Topic.WarrantyClassification) }, { title: \"Service Route\", value: Text(Topic.ServiceRoute) }, { title: \"Recommended Next Action\", value: Text(Topic.RecommendedNextAction) } ] } ], '$schema': \"http://adaptivecards.io/schemas/adaptive-card.json\", version: \"1.5\"}"

    - kind: Question
      id: Question_4ctg8X
      variable: Topic.WarrantySummaryConfirmed
      prompt: Is this information correct?
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_010DcA
      conditions:
        - id: ConditionItem_vzJK96
          condition: =Topic.WarrantySummaryConfirmed = true
          actions:
            - kind: SendActivity
              id: SendActivity_FjPdo2
              activity: Thank you. Your warranty case is now complete.

      elseActions:
        - kind: SendActivity
          id: SendActivity_M8M9Zr
          activity: Please let us know which information you would like to correct. You may update any of the details above.

inputType: {}
outputType: {}