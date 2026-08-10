kind: AdaptiveDialog
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent:
    triggerQueries:
      - troubleshoot my product
      - product isn't working
      - help with device issues
      - fix my appliance
      - safety concern with product
      - my gadget is malfunctioning
      - product troubleshooting guide
      - is this safe to use?
      - step by step troubleshooting help
      - triage a product problem

  actions:
    - kind: SendActivity
      id: SendActivity_XU5XsY
      activity: Welcome to Guided Product Troubleshooting and Safety Triage. I will help you safely troubleshoot your Lenovo ThinkPad E14 Gen 5 laptop or HP LaserJet Pro MFP M428-M429 printer.

    - kind: Question
      id: Question_C5XKJj
      variable: Topic.ProductFamily
      prompt: Which product do you need help with?
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
      id: Question_yqrtvm
      variable: Topic.ProductModel
      prompt: "Please enter your product model (e.g., Lenovo ThinkPad E14 Gen 5 or HP LaserJet Pro MFP M428-M429):"
      entity: StringPrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_oNTW5w
      conditions:
        - id: ConditionItem_lSdXkM
          condition: =Topic.ProductFamily = ProductFamilyOptions.laptop && Topic.ProductModel = "Lenovo ThinkPad E14 Gen 5"
          actions:
            - kind: SendActivity
              id: SendActivity_jhx01v
              activity: "Model supported: Lenovo ThinkPad E14 Gen 5."

        - id: ConditionItem_XVqtMR
          condition: =Topic.ProductFamily = ProductFamilyOptions.printer && Topic.ProductModel = "HP LaserJet Pro MFP M428-M429"
          actions:
            - kind: SendActivity
              id: SendActivity_IBpuzM
              activity: "Model supported: HP LaserJet Pro MFP M428-M429."

      elseActions:
        - kind: SendActivity
          id: SendActivity_MxwepG
          activity: Sorry, this model is not supported for model-specific troubleshooting. I can offer general guidance and recommend contacting human support.

    - kind: Question
      id: Question_5gdKvZ
      variable: Topic.IssueCategory
      prompt: What is the main issue category?
      entity:
        kind: EmbeddedEntity
        definition:
          kind: ClosedListEntity
          optionSetName: IssueCategoryOptions
          items:
            - id: no_power
              displayName: No Power

            - id: charging_failure
              displayName: Charging Failure

            - id: battery_draining
              displayName: Battery Draining

            - id: blank_display
              displayName: Blank Display

            - id: external_display
              displayName: External Display

            - id: overheating
              displayName: Overheating

            - id: wifi_problem
              displayName: WiFi Problem

            - id: keyboard
              displayName: Keyboard

            - id: touchpad
              displayName: Touchpad

            - id: printer_offline
              displayName: Printer Offline

            - id: paper_jam
              displayName: Paper Jam

            - id: poor_print_quality
              displayName: Poor Print Quality

            - id: network_connectivity
              displayName: Network Connectivity

            - id: scan_failure
              displayName: Scan Failure

            - id: toner_warning
              displayName: Toner Warning

            - id: error_message
              displayName: Error Message

    - kind: Question
      id: Question_4oUKCH
      variable: Topic.SymptomDescription
      prompt: Please describe the symptom you are experiencing.
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_3E0fVZ
      variable: Topic.PowerStatus
      prompt: What is the current power status of your device?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_50VfoD
      variable: Topic.ErrorCode
      prompt: Is there any error message or error code displayed?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_8HmWtX
      variable: Topic.IssueStart
      prompt: When did the issue begin?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_2vG3zT
      variable: Topic.IssueFrequency
      prompt: Is the issue intermittent or continuous?
      entity:
        kind: EmbeddedEntity
        definition:
          kind: ClosedListEntity
          optionSetName: IssueFrequencyOptions
          items:
            - id: intermittent
              displayName: Intermittent

            - id: continuous
              displayName: Continuous

    - kind: Question
      id: Question_tNkRzi
      variable: Topic.AttemptedSteps
      prompt: What troubleshooting steps have you already attempted?
      entity: StringPrebuiltEntity

    - kind: Question
      id: Question_6Cvokl
      variable: Topic.PhysicalDamage
      prompt: Is there any visible physical damage?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_PJ14aE
      variable: Topic.LiquidExposure
      prompt: Has the device been exposed to liquid?
      entity: BooleanPrebuiltEntity

    - kind: Question
      id: Question_aZ1ZLn
      variable: Topic.SafetyIndicator
      prompt: Do you notice smoke, sparks, burning smell, excessive heat or electric shock?
      entity: BooleanPrebuiltEntity

    - kind: SendActivity
      id: SendActivity_wh47RQ
      activity: Redirecting to Product Safety Assessment subtopic for safety triage.

    - kind: ConditionGroup
      id: ConditionGroup_f8VBcZ
      conditions:
        - id: ConditionItem_yoAxjm
          condition: =Topic.SafetyIndicator = true
          actions:
            - kind: SendActivity
              id: SendActivity_BAOhvI
              activity: A safety risk has been detected. Please stop using the product immediately. Disconnect power only if it is safe to do so. Do not restart, charge, or dismantle the device. If there is fire, smoke, or electric shock, contact emergency services. We will escalate your case for urgent support.

      elseActions:
        - kind: SendActivity
          id: SendActivity_SThBHk
          activity: No immediate safety risk detected. Proceeding with troubleshooting.

    - kind: Question
      id: Question_bTB6eR
      variable: Topic.ContinueTroubleshooting
      prompt: Would you like to continue troubleshooting?
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_H2KtKj
      conditions:
        - id: ConditionItem_WsXsFv
          condition: =Topic.ContinueTroubleshooting = true && Topic.ProductFamily = ProductFamilyOptions.laptop
          actions:
            - kind: SendActivity
              id: SendActivity_n9uenj
              activity: Starting troubleshooting for your Lenovo ThinkPad E14 Gen 5. I will provide one safe step at a time, based only on Lenovo official sources.

        - id: ConditionItem_GuaUbT
          condition: =Topic.ContinueTroubleshooting = true && Topic.ProductFamily = ProductFamilyOptions.printer
          actions:
            - kind: SendActivity
              id: SendActivity_Dn0PH1
              activity: Starting troubleshooting for your HP LaserJet Pro MFP M428-M429. I will provide one safe step at a time, based only on HP official sources.

      elseActions:
        - kind: SendActivity
          id: SendActivity_5AizGc
          activity: Troubleshooting cancelled by customer. You may contact human technical support for further assistance.

    - kind: Question
      id: Question_1xq7pY
      variable: Topic.TroubleshootingResolved
      prompt: Did this troubleshooting step resolve your issue?
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_Bgl4lN
      conditions:
        - id: ConditionItem_jLMJ0t
          condition: =Topic.TroubleshootingResolved = true
          actions:
            - kind: SendActivity
              id: SendActivity_Nx2j7y
              activity: Great! Your issue appears to be resolved.

      elseActions:
        - kind: SendActivity
          id: SendActivity_1Sibjn
          activity: Let's try the next safe troubleshooting step.

    - kind: Question
      id: Question_lUdQXT
      variable: Topic.CaseSummaryConfirmed
      prompt: |-
        Is the case summary below correct?

        Product Family: {Topic.ProductFamily}
        Product Model: {Topic.ProductModel}
        Issue Category: {Topic.IssueCategory}
        Symptom: {Topic.SymptomDescription}
         
        Troubleshooting Performed: {Topic.AttemptedSteps}
        Resolved: {Topic.TroubleshootingResolved}

        Recommended Next Action: (Based on above)
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: ConditionGroup_BaOD5I
      conditions:
        - id: ConditionItem_aWCtP4
          condition: =Topic.CaseSummaryConfirmed = true
          actions:
            - kind: SendActivity
              id: SendActivity_LJFBGn
              activity: Thank you for confirming. Your case is now complete.

      elseActions:
        - kind: SendActivity
          id: SendActivity_Q8Ca11
          activity: You may correct any information. Let's update the relevant details.

inputType: {}
outputType: {}