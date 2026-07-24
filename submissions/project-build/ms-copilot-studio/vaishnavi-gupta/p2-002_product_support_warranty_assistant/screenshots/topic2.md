kind: AdaptiveDialog
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent:
    triggerQueries:
      - am I eligible for warranty
      - check my warranty status
      - is my product under warranty
      - warranty eligibility check
      - do I qualify for warranty service
      - how do I get my item serviced under warranty
      - service route for my product
      - assess service options for my device
      - can you help with a warranty claim

  actions:
    - kind: Question
      id: Question_zmJ1Hd
      variable: Topic.ProductFamily
      prompt: What is the product family?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_5X9jPu
      variable: Topic.ProductModel
      prompt: What is the product model?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_U33ZHF
      variable: Topic.ItemCategory
      prompt: What is the item category?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_rXaIpF
      variable: Topic.PurchaseDate
      prompt: What is the purchase date?
      entity: DatePrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_OvHXqj
      conditions:
        - id: ConditionItem_65cMVk
          condition: =Topic.PurchaseDate > Today()
          actions:
            - kind: SendActivity
              id: SendActivity_FRscKz
              activity: The purchase date cannot be in the future. Please enter a valid purchase date.

    - kind: Question
      id: Question_xtqk0r
      variable: Topic.DeliveryDate
      prompt: What is the delivery date?
      entity: DatePrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_vcMKmU
      conditions:
        - id: ConditionItem_8r6Dwz
          condition: =Topic.DeliveryDate < Topic.PurchaseDate
          actions:
            - kind: SendActivity
              id: SendActivity_JPszMW
              activity: The delivery date cannot be before the purchase date. Please enter a valid delivery date.

    - kind: Question
      id: Question_RIhSKV
      variable: Topic.PurchasedFromNovaRetail
      prompt: Was the product purchased from NovaRetail?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_8Ur0U6
      variable: Topic.InvoiceAvailable
      prompt: Is the invoice available?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_ZebAT5
      variable: Topic.SerialNumberAvailable
      prompt: Is the serial number available?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_GHtGNn
      variable: Topic.IssueCategory
      prompt: What is the issue category?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_nL9SmN
      variable: Topic.ProductOperational
      prompt: Is the product operational?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_WnGWSr
      variable: Topic.AccidentalDamage
      prompt: Is there accidental damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_K0EW12
      variable: Topic.LiquidDamage
      prompt: Is there liquid damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_oHXAoR
      variable: Topic.ElectricalSurge
      prompt: Is there electrical surge damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_XuJQDf
      variable: Topic.UnauthorizedRepair
      prompt: Has there been any unauthorized repair?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_kL43o9
      variable: Topic.UnauthorizedModification
      prompt: Has there been any unauthorized modification?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_Wqrddq
      variable: Topic.ConsumableInvolved
      prompt: Is a consumable involved?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_zCMu0c
      variable: Topic.ReportedWithinSevenDays
      prompt: Was the issue reported within seven days?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_1uQ0cF
      variable: Topic.TroubleshootingCompleted
      prompt: Has troubleshooting been completed?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_Qnhr42
      variable: Topic.PreviousRepairCount
      prompt: How many previous repairs have been done?
      entity: NumberPrebuiltEntity

    - kind: Question
      id: Question_EFklvH
      variable: Topic.CustomerDisagreesWithAssessment
      prompt: Do you disagree with the assessment?
      entity: BooleanPrebuiltEntity

    - kind: SendActivity
      id: SendActivity_xRMEAK
      activity:
        attachments:
          - kind: AdaptiveCardTemplate
            cardContent: "={ type: \"AdaptiveCard\", body: [ { type: \"TextBlock\", size: \"Medium\", weight: \"Bolder\", text: \"Warranty Assessment Summary\" }, { type: \"FactSet\", facts: [ { title: \"Product Family\", value: Text(Topic.ProductFamily) }, { title: \"Product Model\", value: Text(Topic.ProductModel) }, { title: \"Item Category\", value: Text(Topic.ItemCategory) }, { title: \"Purchase Date\", value: Text(Topic.PurchaseDate) }, { title: \"Delivery Date\", value: Text(Topic.DeliveryDate) }, { title: \"Purchased from NovaRetail\", value: Text(Topic.PurchasedFromNovaRetail) }, { title: \"Invoice Available\", value: Text(Topic.InvoiceAvailable) }, { title: \"Serial Number Available\", value: Text(Topic.SerialNumberAvailable) }, { title: \"Issue Category\", value: Text(Topic.IssueCategory) }, { title: \"Product Operational\", value: Text(Topic.ProductOperational) }, { title: \"Accidental Damage\", value: Text(Topic.AccidentalDamage) }, { title: \"Liquid Damage\", value: Text(Topic.LiquidDamage) }, { title: \"Electrical Surge\", value: Text(Topic.ElectricalSurge) }, { title: \"Unauthorized Repair\", value: Text(Topic.UnauthorizedRepair) }, { title: \"Unauthorized Modification\", value: Text(Topic.UnauthorizedModification) }, { title: \"Consumable Involved\", value: Text(Topic.ConsumableInvolved) }, { title: \"Reported Within Seven Days\", value: Text(Topic.ReportedWithinSevenDays) }, { title: \"Troubleshooting Completed\", value: Text(Topic.TroubleshootingCompleted) }, { title: \"Previous Repair Count\", value: Text(Topic.PreviousRepairCount) }, { title: \"Customer Disagrees With Assessment\", value: Text(Topic.CustomerDisagreesWithAssessment) } ] } ], '$schema': \"http://adaptivecards.io/schemas/adaptive-card.json\", version: \"1.5\" }"

inputType: {}
outputType: {}