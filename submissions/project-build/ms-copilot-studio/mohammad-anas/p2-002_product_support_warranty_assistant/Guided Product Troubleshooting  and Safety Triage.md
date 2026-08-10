kind: AdaptiveDialog
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent:
    triggerQueries:
      - help with product troubleshooting
      - product isn't working
      - troubleshoot my device
      - fix my product issue
      - product safety concern
      - is this product safe to use?
      - guide me through troubleshooting steps
      - my device is malfunctioning
      - safety triage for my product
      - need help with a faulty product

  actions:
    - kind: SendActivity
      id: Welcome
      activity: Welcome to the troubleshooting assistant. I can help with Lenovo ThinkPad E14 laptops and HP LaserJet Pro M428-M429 printers.

    - kind: Question
      id: AskProduct
      variable: Topic.ProductModel
      prompt: Which product are you having trouble with?
      entity:
        kind: EmbeddedEntity
        definition:
          kind: ClosedListEntity
          optionSetName: SupportedProducts
          items:
            - id: thinkpad_e14
              displayName: Lenovo ThinkPad E14

            - id: hp_laserjet_pro
              displayName: HP LaserJet Pro M428-M429

    - kind: ConditionGroup
      id: ProductCheck
      conditions:
        - id: Supported
          condition: =Topic.ProductModel = SupportedProducts.thinkpad_e14 || Topic.ProductModel = SupportedProducts.hp_laserjet_pro
          actions:
            - kind: SendActivity
              id: SafetyIntro
              activity: Before troubleshooting, I need to perform a quick safety assessment.

            - kind: Question
              id: AskSafety
              variable: Topic.SafetyIssue
              prompt: Are there smoke, sparks, fire, burning smell, electric shock, excessive heat, swollen battery, exposed wiring, melting parts, or liquid exposure?
              entity: BooleanPrebuiltEntity

            - kind: ConditionGroup
              id: SafetyCheck
              conditions:
                - id: IsSafetyIssue
                  condition: =Topic.SafetyIssue
                  actions:
                    - kind: SetVariable
                      id: SetSafetyEscalation
                      variable: Topic.EscalationLevel
                      value: Level 4 - Safety Critical

                    - kind: SendActivity
                      id: SafetyStop
                      activity: Stop using the device immediately. Disconnect power only if it is safe to do so. Your case has been escalated to the safety team.

                    - kind: EndDialog
                      id: EndSafetyDialog

              elseActions:
                - kind: Question
                  id: AskSymptom
                  variable: Topic.SymptomDescription
                  prompt: Please describe the issue.
                  entity: StringPrebuiltEntity

                - kind: Question
                  id: AskIssueStart
                  variable: Topic.IssueStart
                  prompt: When did the issue start?
                  entity: DatePrebuiltEntity

                - kind: Question
                  id: AskResolved
                  variable: Topic.TroubleshootingResolved
                  prompt: Did the suggested troubleshooting step resolve the issue?
                  entity: BooleanPrebuiltEntity

                - kind: ConditionGroup
                  id: ResolutionCheck
                  conditions:
                    - id: Resolved
                      condition: =Topic.TroubleshootingResolved
                      actions:
                        - kind: SetVariable
                          id: SetResolved
                          variable: Topic.EscalationLevel
                          value: Level 1 - Self Service

                        - kind: SendActivity
                          id: ResolvedMessage
                          activity: Great! Your issue appears to be resolved.

                  elseActions:
                    - kind: SetVariable
                      id: SetEscalate
                      variable: Topic.EscalationLevel
                      value: Level 2 - Technical Support

                    - kind: SendActivity
                      id: EscalateMessage
                      activity: Your issue requires further technical assistance and will be escalated.

                - kind: EndDialog
                  id: EndNormalDialog

      elseActions:
        - kind: SetVariable
          id: UnsupportedEscalation
          variable: Topic.EscalationLevel
          value: Level 3 - Unsupported Product

        - kind: SendActivity
          id: UnsupportedMessage
          activity: Sorry, only Lenovo ThinkPad E14 laptops and HP LaserJet Pro M428-M429 printers are supported.

        - kind: EndDialog
          id: EndUnsupported

inputType: {}
outputType: {}