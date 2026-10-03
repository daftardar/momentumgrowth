// Momentum Growth website — contact form backend (Google Apps Script)
// Deploy: Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone
// Owner: personal account. Sheet is shared with the company accounts listed in SHARE_WITH.

var SHEET_ID = '1anepNDRh2GzcQ2dQ3KhTZeaOzLnexh4RVAhn-8J7_ok';
var SHEET_NAME = 'طلبات موقع مومينتوم جروث';
var NOTIFY_EMAIL = 'info@momentumgrowth.com.sa';
var SHARE_WITH = ['yahya@momentumgrowth.com.sa', 'info@momentumgrowth.com.sa'];
var HEADERS = ['التاريخ والوقت', 'الاسم', 'المنشأة', 'البريد الإلكتروني', 'الجوال', 'الخدمة المطلوبة', 'الرسالة', 'لغة الصفحة'];

function getSheet_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID') || SHEET_ID;
  var ss = null;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
  if (!ss) {
    ss = SpreadsheetApp.create(SHEET_NAME);
    var sh = ss.getSheets()[0];
    sh.setName('الطلبات');
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#13254A').setFontColor('#FFFFFF');
    sh.setFrozenRows(1);
    sh.setRightToLeft(true);
    props.setProperty('SHEET_ID', ss.getId());
  }
  if (!props.getProperty('SHARED')) {
    try { ss.addEditors(SHARE_WITH); } catch (e3) {}
    var first = ss.getSheets()[0];
    first.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#13254A').setFontColor('#FFFFFF');
    first.setFrozenRows(1); first.setRightToLeft(true);
    props.setProperty('SHARED', '1');
  }
  return ss;
}

function doPost(e) {
  try {
    var p = e.parameter || {};
    var ss = getSheet_();
    var sheet = ss.getSheets()[0];
    var now = new Date();
    sheet.appendRow([
      Utilities.formatDate(now, 'Asia/Riyadh', 'yyyy-MM-dd HH:mm'),
      p.name || '', p.company || '', p.email || '', (p.phone ? "'" + p.phone : ''),
      p.service || '', p.message || '', p.lang || 'ar'
    ]);
    var body =
      'طلب جديد من الموقع\n\n' +
      'الاسم: ' + (p.name || '') + '\n' +
      'المنشأة: ' + (p.company || '') + '\n' +
      'البريد: ' + (p.email || '') + '\n' +
      'الجوال: ' + (p.phone || '') + '\n' +
      'الخدمة: ' + (p.service || '') + '\n\n' +
      'الرسالة:\n' + (p.message || '') + '\n\n' +
      'الجدول: ' + ss.getUrl();
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: 'طلب تواصل من الموقع - ' + (p.name || ''),
      body: body,
      replyTo: p.email || NOTIFY_EMAIL
    });
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('Momentum Growth form endpoint is live.');
}

// Run this once from the editor to create the sheet and grant permissions.
function setup() {
  var ss = getSheet_();
  Logger.log(ss.getUrl());
}
