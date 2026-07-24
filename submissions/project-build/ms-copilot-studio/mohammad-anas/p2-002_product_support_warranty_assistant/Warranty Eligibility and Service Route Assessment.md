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
      - can I get service under warranty
      - do I qualify for a warranty repair
      - service route assessment

  actions:
    - kind: Question
      id: AskProduct
      variable: Topic.ProductModel
      prompt: Select your product.
      entity: StringPrebuiltEntity

    - kind: Question
      id: AskCategory
      variable: Topic.ItemCategory
      prompt: What type of item is this?
      entity:
        kind: EmbeddedEntity
        definition:
          kind: ClosedListEntity
          optionSetName: ItemCategoryOptions
          items:
            - id: laptop
              displayName: Laptop

            - id: printer
              displayName: Printer

            - id: battery
              displayName: Battery

            - id: accessory
              displayName: Accessory

            - id: consumable
              displayName: Consumable

    - kind: Question
      id: AskPurchaseDate
      variable: Topic.PurchaseDate
      prompt: What is the purchase date?
      entity: DatePrebuiltEntity

    - kind: Question
      id: AskDeliveryDate
      variable: Topic.DeliveryDate
      prompt: What is the delivery date?
      entity: DatePrebuiltEntity

    - kind: ConditionGroup
      id: ValidateDates
      conditions:
        - id: FuturePurchase
          condition: =Topic.PurchaseDate > Today()
          actions:
            - kind: SendActivity
              id: PurchaseError
              activity: Purchase date cannot be in the future.

            - kind: EndDialog
              id: EndFuturePurchase

        - id: DeliveryBeforePurchase
          condition: =Topic.DeliveryDate < Topic.PurchaseDate
          actions:
            - kind: SendActivity
              id: DeliveryError
              activity: Delivery date cannot be before the purchase date.

            - kind: EndDialog
              id: EndDeliveryError

    - kind: Question
      id: AskTroubleshooting
      variable: Topic.TroubleshootingDone
      prompt: Has approved troubleshooting been completed?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: AskIssueCategory
      variable: Topic.IssueCategory
      prompt: What is the issue category?
      entity: StringPrebuiltEntity

    - kind: ConditionGroup
      id: TroubleshootingCheck
      conditions:
        - id: NeedsTroubleshooting
          condition: =And(Not(Topic.TroubleshootingDone), Topic.IssueCategory <> "safety")
          actions:
            - kind: SendActivity
              id: RedirectMessage
              activity: Please complete Guided Product Troubleshooting before continuing this assessment.

            - kind: EndDialog
              id: EndRedirect

        - id: SafetyIssue
          condition: =Topic.IssueCategory = "safety"
          actions:
            - kind: SendActivity
              id: SafetyEscalation
              activity: Safety issue detected. Escalating to the safety team.

            - kind: EndDialog
              id: EndSafety

    - kind: Question
      id: AskAccidentalDamage
      variable: Topic.AccidentalDamage
      prompt: Has the product suffered accidental damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: AskLiquidDamage
      variable: Topic.LiquidDamage
      prompt: Has the product been exposed to liquid?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: AskElectricalSurge
      variable: Topic.ElectricalSurge
      prompt: Has the product experienced an electrical surge?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: AskUnauthorizedRepair
      variable: Topic.UnauthorisedRepair
      prompt: Has the product been repaired by an unauthorised party?
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: WarrantyAssessment
      conditions:
        - id: Exclusion
          condition: =Or(Topic.AccidentalDamage, Topic.LiquidDamage, Topic.ElectricalSurge, Topic.UnauthorisedRepair)
          actions:
            - kind: SendActivity
              id: ExclusionMessage
              activity: Your case may fall under a warranty exclusion and will require human review.

      elseActions:
        - kind: SendActivity
          id: PreliminaryMessage
          activity: Your warranty assessment has been completed. This is a preliminary result pending human review.

    - kind: EndDialog
      id: EndAssessment

inputType: {}
outputType: {}