export interface SendEmailPayload {
  to: string;
  from?: string;
  subject: string;
  textContent: string;
  htmlContent?: string;
  reportType?: string;
  anomalyId?: string;
  skuId?: string;
}

export interface SendEmailResult {
  success: boolean;
  messageId: string;
  recipient: string;
  sender: string;
  timestamp: string;
  status: string;
}

export async function sendEmail(
  payload: SendEmailPayload
): Promise<SendEmailResult> {
  console.log('=== EMAIL SERVICE DEBUG ===');
  console.log('Sending email via Django backend');
  console.log('Payload:', payload);
  console.log('Endpoint: /api/email/send');
  console.log('========================');

  try {
    const requestBody = {
      to: payload.to,
      from_email: payload.from,
      subject: payload.subject,
      text_content: payload.textContent,
      html_content: payload.htmlContent,
      report_type: payload.reportType,
      anomaly_id: payload.anomalyId,
      sku_id: payload.skuId
    };

    console.log('Request body:', requestBody);

    const response = await fetch('/api/email/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      let errorMessage = `Email delivery failed with status ${response.status}`;
      try {
        const error = await response.json();
        console.error('Error response:', error);
        errorMessage = error.error || errorMessage;
      } catch (parseError) {
        console.error('Could not parse error response as JSON:', parseError);
        errorMessage = `Backend error (${response.status}). Check backend logs for details.`;
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    console.log('Success response:', data);

    const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }) + ' IST';

    const result = {
      success: true,
      messageId: data.messageId || `msg_${Date.now()}`,
      recipient: payload.to,
      sender: payload.from || 'noreply@agileventures.net',
      timestamp: data.timestamp || timestamp,
      status: 'Email sent successfully via SMTP'
    };

    console.log('=== EMAIL SENT SUCCESSFULLY ===');
    console.log('Result:', result);

    return result;
  } catch (error) {
    console.error('=== EMAIL SEND FAILED ===');
    console.error('Error:', error);
    throw error;
  }
}
