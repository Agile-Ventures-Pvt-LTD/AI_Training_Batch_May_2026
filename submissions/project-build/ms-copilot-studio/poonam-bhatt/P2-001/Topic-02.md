kind: AdaptiveDialog
modelDescription: Use this topic whenever a user reports or seeks guidance about workplace concerns such as harassment, bullying, discrimination, retaliation, grievances, inappropriate behaviour, safety concerns, or confidential HR reporting. Prioritize immediate safety, avoid requesting sensitive personal information or detailed incident descriptions, provide confidential HR escalation guidance, and remind the user that the chatbot is not an emergency or investigative service.
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent: {}
  actions:
    - kind: SendActivity
      id: sendActivity_ZHdhTz
      activity: I'm sorry you're experiencing this.  I'm here to provide guidance on the appropriate reporting process.  I cannot investigate complaints, but I can help explain the available support options.

    - kind: Question
      id: question_D3Vt5O
      interruptionPolicy:
        allowInterruption: true

      variable: init:Topic.IsImmediateDanger
      prompt: Is anyone currently in immediate danger?
      entity: BooleanPrebuiltEntity

    - kind: ConditionGroup
      id: conditionGroup_BXmMmY
      conditions:
        - id: conditionItem_mzyE9f
          condition: =Topic.IsImmediateDanger = true
          actions:
            - kind: SendActivity
              id: sendActivity_3cr9xz
              activity: |-
                Your safety is the highest priority.
                • Move to a safe location.
                • Contact local emergency services or workplace security immediately if needed.
                • Inform an authorised manager or HR representative when it is safe to do so.
                I'm unable to provide emergency assistance directly.

      elseActions:
        - kind: Question
          id: question_RoLqQL
          interruptionPolicy:
            allowInterruption: true

          variable: init:Topic.ConcernType
          prompt: Which best describes your concern?
          entity:
            kind: EmbeddedEntity
            definition:
              kind: ClosedListEntity
              items:
                - id: Harassment
                  displayName: Harassment

                - id: Discrimination
                  displayName: Discrimination

                - id: retaliation
                  displayName: retaliation

                - id: bullying
                  displayName: bullying

                - id: "General Workplace Conflict "
                  displayName: "General Workplace Conflict "

                - id: others
                  displayName: others

        - kind: SendActivity
          id: sendActivity_9ChvWQ
          activity: |-
            You don't need to share detailed descriptions or sensitive personal information here.
            Your privacy is important.

        - kind: Question
          id: question_CyKSRg
          interruptionPolicy:
            allowInterruption: true

          variable: init:Topic.WantsHREscalation
          prompt: Would you like confidential HR escalation information?
          entity: BooleanPrebuiltEntity

        - kind: ConditionGroup
          id: conditionGroup_TkrchP
          conditions:
            - id: conditionItem_LfGgfL
              condition: =Topic.ConcernType = 'cr034_PoonamNovaHRAssist.topic.Topic-02WorkplaceconcernEscalation.main.question_RoLqQL'.Harassment
              actions:
                - kind: SendActivity
                  id: sendActivity_2WmYEm
                  activity: |-
                    This type of concern should be reported confidentially through the appropriate HR channel or Internal Committee.

                    The chatbot cannot determine whether misconduct has occurred or predict the outcome of any investigation.

                    An authorised HR representative will guide you through the official process.

            - id: conditionItem_ylH58S
              condition: =Topic.ConcernType = 'cr034_PoonamNovaHRAssist.topic.Topic-02WorkplaceconcernEscalation.main.question_RoLqQL'.Discrimination
              actions:
                - kind: SendActivity
                  id: sendActivity_BOmEnV
                  activity: |-
                    This type of concern should be reported confidentially through the appropriate HR channel or Internal Committee.

                    The chatbot cannot determine whether misconduct has occurred or predict the outcome of any investigation.

                    An authorised HR representative will guide you through the official process.

            - id: conditionItem_elDLdC
              condition: =Topic.ConcernType = 'cr034_PoonamNovaHRAssist.topic.Topic-02WorkplaceconcernEscalation.main.question_RoLqQL'.retaliation
              actions:
                - kind: SendActivity
                  id: sendActivity_424vP7
                  activity: |-
                    This type of concern should be reported confidentially through the appropriate HR channel or Internal Committee.

                    The chatbot cannot determine whether misconduct has occurred or predict the outcome of any investigation.

                    An authorised HR representative will guide you through the official process.

            - id: conditionItem_erkZYD
              condition: =Topic.ConcernType = 'cr034_PoonamNovaHRAssist.topic.Topic-02WorkplaceconcernEscalation.main.question_RoLqQL'.bullying
              actions:
                - kind: SendActivity
                  id: sendActivity_Xf3355
                  activity: |-
                    Bullying concerns should be reported confidentially to HR or your designated HR Business Partner.
                    The appropriate team can explain the reporting process and available support.

            - id: conditionItem_7U5UQA
              condition: =Topic.ConcernType = 'cr034_PoonamNovaHRAssist.topic.Topic-02WorkplaceconcernEscalation.main.question_RoLqQL'.'General Workplace Conflict '
              actions:
                - kind: SendActivity
                  id: sendActivity_3KViAL
                  activity: |-
                    If appropriate, consider discussing the issue with your manager.
                    If the concern cannot be resolved, you may contact your HR Business Partner or use the formal grievance process.

            - id: conditionItem_pCHVPF
              condition: =Topic.ConcernType = 'cr034_PoonamNovaHRAssist.topic.Topic-02WorkplaceconcernEscalation.main.question_RoLqQL'.others
              actions:
                - kind: SendActivity
                  id: sendActivity_O89pOH
                  activity: |-
                    Your concern may require support from HR.
                    Please contact the HR department for confidential guidance.

    - kind: SendActivity
      id: sendActivity_ehShF1
      activity: |-
        Please do not share sensitive personal information such as:
        • Aadhaar numbers
        • Banking information
        • Passwords
        • Medical reports
        • Evidence files
        • Witness names
        These details should only be shared through authorised HR procedures if requested.

    - kind: SendActivity
      id: sendActivity_bgMupZ
      activity: |-
        Thank you for reaching out.
        I'm here to provide general guidance, but I am not an emergency or investigative service.
        If you would like to proceed, please contact the appropriate HR representative or Internal Committee using the official reporting channels.

    - kind: CancelAllDialogs
      id: XEgBqL

inputType: {}
outputType: {}