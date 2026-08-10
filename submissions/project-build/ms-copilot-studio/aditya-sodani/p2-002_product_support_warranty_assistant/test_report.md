# Test Report

## Project

**Product Support and Warranty Assistant (NovaRetail Support
Assistant)**

## Test Summary

  Metric                        Value
  --------------------------- -------
  Total Test Cases Executed        30
  Passed                           26
  Failed                            4
  Pass Rate                     86.7%

## Execution Result

  -----------------------------------------------------------------------
  ID                      Scenario                Result
  ----------------------- ----------------------- -----------------------
  TC-01                   My Lenovo ThinkPad E14  Pass
                          Gen 5 won't turn on.    
                          What should I do?       

  TC-02                   How can I check if my   Fail
                          HP LaserJet Pro MFP     
                          M428 is still under     
                          warranty?               

  TC-03                   The power cable for my  Pass
                          HP printer is getting   
                          very hot. Is this safe? 

  TC-04                   Can you help me set up  Pass
                          my ThinkPad E16 Gen 1   
                          for the first time?     

  TC-05                   I spilled water on my   Pass
                          Lenovo laptop. What     
                          should I do now?        

  TC-06                   My HP printer keeps     Pass
                          showing a paper jam     
                          error, but there's no   
                          paper stuck. Any        
                          advice?                 

  TC-07                   How do I find the       Pass
                          serial number on my     
                          ThinkPad E14 Gen 5?     

  TC-08                   Is the charger that     Pass
                          came with my Lenovo     
                          laptop covered under    
                          warranty?               

  TC-09                   My printer is making a  Pass
                          burning smell. Should I 
                          keep using it?          

  TC-10                   What's the difference   Pass
                          between the ThinkPad    
                          E14 Gen 5 and E16 Gen   
                          1?                      

  TC-11                   Can you help me connect Pass
                          my HP LaserJet Pro MFP  
                          M429 to Wi-Fi?          

  TC-12                   My Lenovo laptop        Pass
                          battery looks swollen.  
                          What should I do?       

  TC-13                   How do I get support if Pass
                          my product isn't listed 
                          here?                   

  TC-14                   I'm not sure if my      Pass
                          issue is with the       
                          laptop or the charger.  
                          Can you help me figure  
                          it out?                 

  TC-15                   My HP printer won't     Pass
                          print and is showing an 
                          error code. What does   
                          it mean?                

  TC-16                   Can you tell me if      Pass
                          accidental damage is    
                          covered by the NovaCare 
                          Limited Warranty?       

  TC-17                   I need to speak to a    Fail
                          human representative    
                          about my warranty. Can  
                          you connect me?         

  TC-18                   My ThinkPad E16 Gen 1   Pass
                          is overheating. What    
                          steps should I take?    

  TC-19                   How do I safely clean   Pass
                          my HP printer?          

  TC-20                   I have both a Lenovo    Pass
                          laptop and an HP        
                          printer with issues.    
                          Can you help with both? 

  TC-21                   My ThinkPad E14 Gen 5   Pass
                          won't turn on. What     
                          should I do?            

  TC-22                   How can I check if my   Fail
                          HP LaserJet Pro MFP     
                          M428 is still under     
                          warranty?               

  TC-23                   The power cable for my  Pass
                          HP printer is getting   
                          very hot. Is this safe? 

  TC-24                   Can you help me set up  Pass
                          my new ThinkPad E16 Gen 
                          1?                      

  TC-25                   I spilled water on my   Pass
                          Lenovo laptop. What     
                          steps should I take     
                          now?                    

  TC-26                   My HP printer keeps     Pass
                          showing a paper jam     
                          error, but there's no   
                          paper stuck. Any        
                          suggestions?            

  TC-27                   Is the charger that     Fail
                          came with my ThinkPad   
                          E14 Gen 5 covered under 
                          warranty?               

  TC-28                   I'm not sure if my      Pass
                          issue is with the       
                          laptop or the charger.  
                          Can you help me figure  
                          it out?                 

  TC-29                   What should I do if my  Pass
                          ThinkPad E16 Gen 1      
                          battery looks swollen?  

  TC-30                   Can you tell me the     Pass
                          difference between the  
                          ThinkPad E14 Gen 5 and  
                          E16 Gen 1?              
  -----------------------------------------------------------------------

## Failed Test Cases

  -----------------------------------------------------------------------
  Scenario                            Failure Reason
  ----------------------------------- -----------------------------------
  How can I check if my HP LaserJet   Not answered: The agent response
  Pro MFP M428 is still under         did not provide the actual steps to
  warranty?                           check the warranty and only asked
                                      the user to select a product
                                      family, leaving the question
                                      unanswered. Because the agent
                                      didn't answer the question, the
                                      response wasn't evaluated for
                                      relevance, completeness, or use of
                                      knowledge sources.

  I need to speak to a human          Not answered: The agent says it
  representative about my warranty.   cannot connect to a human
  Can you connect me?                 representative and does not offer
                                      any useful alternative, only
                                      explaining what could happen in
                                      theory. Because the agent didn't
                                      answer the question, the response
                                      wasn't evaluated for relevance,
                                      completeness, or use of knowledge
                                      sources.

  How can I check if my HP LaserJet   Not answered: The agent response
  Pro MFP M428 is still under         does not provide the actual steps
  warranty?                           to check the warranty. It only asks
                                      the user to select a product
                                      family, which does not answer the
                                      main question. Because the agent
                                      didn't answer the question, the
                                      response wasn't evaluated for
                                      relevance, completeness, or use of
                                      knowledge sources.

  Is the charger that came with my    Not answered: The agent response
  ThinkPad E14 Gen 5 covered under    does not answer the user's question
  warranty?                           about warranty coverage and only
                                      asks the user to select their
                                      product family. This means it does
                                      not provide any actual information.
                                      Because the agent didn't answer the
                                      question, the response wasn't
                                      evaluated for relevance,
                                      completeness, or use of knowledge
                                      sources.
  -----------------------------------------------------------------------

## Observations

-   The chatbot successfully handled most product support and safety
    scenarios.
-   Safety-related conversations (burning smell, swollen battery, liquid
    damage, paper jam, etc.) passed successfully.
-   Troubleshooting workflows for Lenovo laptops and HP printers behaved
    as expected.
-   The primary failures occurred in warranty-related conversations
    where the agent immediately entered the warranty assessment flow
    instead of first answering the user's direct question.
-   Human handoff messaging requires improvement by providing clear
    contact instructions rather than stating that escalation is not
    configured.

## Recommendations

1.  Improve warranty question handling before starting the assessment
    flow.
2.  Provide informative responses for warranty coverage questions before
    requesting additional details.
3.  Improve human support escalation with contact options.
4.  Continue validating against all 40 mandatory project test cases.

## Conclusion

A total of **30** evaluation scenarios were executed.

**26** scenarios passed successfully and **4** scenarios failed,
resulting in an overall **pass rate of 86.7%**.

The assistant demonstrates stable troubleshooting behaviour and strong
safety handling. Future improvements should focus on warranty enquiries,
customer escalation flows, and direct informational responses.
