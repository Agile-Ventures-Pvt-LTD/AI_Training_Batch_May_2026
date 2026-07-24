kind: AdaptiveDialog
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent:
    triggerQueries:
      - tell me about topic 01
      - what is topic-01
      - explain topic one
      - information on topic-01
      - details about topic one
      - topic-01 overview
      - learn about topic one
      - describe topic-01
      - topic one info

  actions:
    - kind: Question
      id: Question_AcGbWF
      variable: Topic.ProductFamily
      prompt: Welcome to Guided Product Troubleshooting and Safety Triage. What type of product are you having issues with?
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
      id: Question_9RuFPM
      variable: Topic.ProductModel
      prompt: Please provide your product model.
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_ZRAIdm
      variable: Topic.IssueCategory
      prompt: Please select the issue category.
      entity:
        kind: EmbeddedEntity
        definition:
          kind: ClosedListEntity
          optionSetName: IssueCategoryOptions
          items:
            - id: power
              displayName: Power/No Power

            - id: charging
              displayName: Charging/Battery

            - id: display
              displayName: Display/Screen

            - id: wifi
              displayName: Wi-Fi/Connectivity

            - id: keyboard
              displayName: Keyboard/Touchpad

            - id: printer_offline
              displayName: Printer Offline

            - id: paper_jam
              displayName: Paper Jam

            - id: print_quality
              displayName: Poor Print Quality

            - id: scan_failure
              displayName: Scan Failure

            - id: toner_warning
              displayName: Toner Warning

            - id: error_message
              displayName: Error Message

    - kind: Question
      id: Question_M0kwWk
      variable: Topic.SymptomDescription
      prompt: Please briefly describe the symptom.
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_ikKG4J
      variable: Topic.PowerStatus
      prompt: Is the device currently powered on?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_hjcWth
      variable: Topic.ErrorCode
      prompt: If you see an error code, please enter it. If not, type 'None'.
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_1y2hJk
      variable: Topic.IssueStart
      prompt: When did the issue start?
      entity: DateTimePrebuiltEntity

    - kind: Question
      id: Question_eeGQPw
      variable: Topic.IssueFrequency
      prompt: How often does the issue occur?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_1OhjQo
      variable: Topic.AttemptedSteps
      prompt: Have you already tried any troubleshooting steps? If yes, please list them.
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_VOFg2w
      variable: Topic.PhysicalDamage
      prompt: Is there any visible physical damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_52Wlhp
      variable: Topic.LiquidExposure
      prompt: Has the device been exposed to liquid?
      entity: BooleanPrebuiltEntity

    - kind: SendActivity
      id: SendActivity_tDicRp
      activity: Before we begin troubleshooting, we need to perform a safety assessment.

    - kind: SendActivity
      id: SendActivity_uoq9R2
      activity: "Calling reusable topic: Product Safety Assessment..."

    - kind: ConditionGroup
      id: ConditionGroup_sEHkHT
      conditions:
        - id: ConditionItem_bU5FmR
          condition: =Topic.SafetyLevel = "Level 4"
          actions:
            - kind: SendActivity
              id: SendActivity_dSUYPq
              activity: A critical safety issue has been detected. Please unplug the device immediately and do not attempt further troubleshooting. Contact support for further instructions.

            - kind: SendActivity
              id: SendActivity_m7TyAf
              activity: Escalating your case for urgent safety review.

      elseActions:
        - kind: ConditionGroup
          id: ConditionGroup_QEuOt7
          conditions:
            - id: ConditionItem_ei8K78
              condition: =Topic.ProductFamily = ProductFamilyOptions.Laptop
              actions:
                - kind: ConditionGroup
                  id: ConditionGroup_qZA6uL
                  conditions:
                    - id: ConditionItem_yUXv5O
                      condition: =Topic.ProductModel = "Lenovo ThinkPad E14 Gen 5"
                      actions:
                        - kind: SendActivity
                          id: SendActivity_O36agM
                          activity: Supported Lenovo ThinkPad E14 Gen 5 detected. Proceeding with model-specific troubleshooting.

                        - kind: ConditionGroup
                          id: ConditionGroup_jikiSA
                          conditions:
                            - id: ConditionItem_oj3WEk
                              condition: =Topic.IssueCategory = IssueCategoryOptions.power
                              actions:
                                - kind: SendActivity
                                  id: SendActivity_OY61zl
                                  activity: Generating safe troubleshooting steps for power issues using Lenovo Support documentation.

                                - kind: Question
                                  id: Question_7V6NDk
                                  variable: Topic.TroubleshootingResolved
                                  prompt: Did this resolve your issue?
                                  entity: BooleanPrebuiltEntity

                                - kind: ConditionGroup
                                  id: ConditionGroup_iORUnF
                                  conditions:
                                    - id: ConditionItem_uoCZuY
                                      condition: =Topic.TroubleshootingResolved = true
                                      actions:
                                        - kind: SendActivity
                                          id: SendActivity_bhmp9k
                                          activity: Issue resolved. Generating support case summary.

                                        - kind: SendActivity
                                          id: SendActivity_W5CCA7
                                          activity: "Calling reusable topic: Support Case Summary."

                                  elseActions:
                                    - kind: SendActivity
                                      id: SendActivity_5DvHJ0
                                      activity: Let's try another step. Increasing troubleshooting step count.

                                    - kind: SendActivity
                                      id: SendActivity_uuIr0o
                                      activity: If the issue is not resolved after 3 steps, we will escalate to technical support.

                          elseActions:
                            - kind: SendActivity
                              id: SendActivity_KLX8HK
                              activity: Unsupported issue category for this model. Please contact support for further assistance.

                  elseActions:
                    - kind: SendActivity
                      id: SendActivity_bpFXew
                      activity: This laptop model is not supported for model-specific troubleshooting. We can provide general guidance and escalate your case to human support.

            - id: ConditionItem_rosEUo
              condition: =Topic.ProductFamily = ProductFamilyOptions.printer
              actions:
                - kind: ConditionGroup
                  id: ConditionGroup_Fa8LGa
                  conditions:
                    - id: ConditionItem_0rcNu2
                      condition: =Topic.ProductModel = "HP LaserJet Pro MFP M428-M429"
                      actions:
                        - kind: SendActivity
                          id: SendActivity_dvn7HR
                          activity: Supported HP LaserJet Pro MFP M428-M429 detected. Proceeding with model-specific troubleshooting.

                        - kind: ConditionGroup
                          id: ConditionGroup_7TkdEZ
                          conditions:
                            - id: ConditionItem_R2d6we
                              condition: =Topic.IssueCategory = IssueCategoryOptions.paper_jam
                              actions:
                                - kind: SendActivity
                                  id: SendActivity_EA6QgT
                                  activity: Generating safe troubleshooting steps for paper jam using HP documentation.

                                - kind: Question
                                  id: Question_r3np4Y
                                  variable: Topic.TroubleshootingResolved
                                  prompt: Did this resolve your issue?
                                  entity: BooleanPrebuiltEntity

                                - kind: ConditionGroup
                                  id: ConditionGroup_hzokpL
                                  conditions:
                                    - id: ConditionItem_BoWYSK
                                      condition: =Topic.TroubleshootingResolved = true
                                      actions:
                                        - kind: SendActivity
                                          id: SendActivity_fwrlSr
                                          activity: Issue resolved. Generating support case summary.

                                        - kind: SendActivity
                                          id: SendActivity_KmyZDt
                                          activity: "Calling reusable topic: Support Case Summary."

                                  elseActions:
                                    - kind: SendActivity
                                      id: SendActivity_keixTd
                                      activity: Let's try another step. Increasing troubleshooting step count.

                                    - kind: SendActivity
                                      id: SendActivity_0Z3qP1
                                      activity: If the issue is not resolved after 3 steps, we will escalate to technical support.

                          elseActions:
                            - kind: SendActivity
                              id: SendActivity_co7MP2
                              activity: Unsupported issue category for this model. Please contact support for further assistance.

                  elseActions:
                    - kind: SendActivity
                      id: SendActivity_ydX71O
                      activity: This printer model is not supported for model-specific troubleshooting. We can provide general guidance and escalate your case to human support.

          elseActions:
            - kind: SendActivity
              id: SendActivity_gnJBt5
              activity: Unsupported product family. Please contact support for further assistance.

    - kind: SendActivity
      id: SendActivity_GfxsHy
      activity:
        attachments:
          - kind: AdaptiveCardTemplate
            cardContent: "={ type: \"AdaptiveCard\", body: [ { type: \"TextBlock\", size: \"Medium\", weight: \"Bolder\", text: \"Support Case Summary\" }, { type: \"FactSet\", facts: [ { title: \"Product Family\", value: Text(Topic.ProductFamily) }, { title: \"Product Model\", value: Text(Topic.ProductModel) }, { title: \"Issue Category\", value: Text(Topic.IssueCategory) }, { title: \"Symptom\", value: Text(Topic.SymptomDescription) }, { title: \"Safety Classification\", value: Text(Topic.SafetyLevel) }, { title: \"Troubleshooting Performed\", value: Text(Topic.AttemptedSteps) }, { title: \"Outcome\", value: Text(Topic.TroubleshootingResolved) }, { title: \"Escalation Level\", value: Text(Topic.EscalationLevel) } ] } ], '$schema': \"http://adaptivecards.io/schemas/adaptive-card.json\", version: \"1.5\"}"

    - kind: Question
      id: Question_3wMKwZ
      variable: Topic.CaseSummaryConfirmed
      prompt: Would you like to confirm this summary or make corrections?
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_SGgY7z
      conditions:
        - id: ConditionItem_sxtbqx
          condition: =Topic.CaseSummaryConfirmed = false
          actions:
            - kind: SendActivity
              id: SendActivity_rwWyrG
              activity: You can correct the product family, model, issue category, safety answers, or troubleshooting result. Please specify what you'd like to update.

      elseActions:
        - kind: SendActivity
          id: SendActivity_d0qBcC
          activity: Thank you. Your case has been updated and will be processed according to NovaCare policies.

    - kind: SendActivity
      id: SendActivity_gqPwpS
      activity: A critical safety issue has been detected. Please unplug the device immediately and do not attempt further troubleshooting. Contact support for further instructions.

    - kind: SendActivity
      id: SendActivity_YwSkO8
      activity: Escalating your case for urgent safety review.

    - kind: SendActivity
      id: SendActivity_xMI2RP
      activity: A critical safety issue has been detected. Please unplug the device immediately and do not attempt further troubleshooting. Contact support for further instructions.

    - kind: SendActivity
      id: SendActivity_rSZ3ya
      activity: Escalating your case for urgent safety review.

inputType: {}
outputType: {}