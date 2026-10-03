# -*- coding: utf-8 -*-
"""Generate website/en/index.html from the Arabic preview page."""
import io, re, os, sys
src = r'C:\Users\yahya\OneDrive\Desktop\شركة مومينتوم جروث\website\index.html'
out_dir = r'C:\Users\yahya\OneDrive\Desktop\شركة مومينتوم جروث\website\en'
os.makedirs(out_dir, exist_ok=True)
s = io.open(src, encoding='utf-8').read()

T = {
# ---- head ----
'<html lang="ar" dir="rtl">': '<html lang="en" dir="ltr">',
'<title>مومينتوم جروث | Momentum Growth</title>': '<title>Momentum Growth | مومينتوم جروث</title>',
'content="شركة مومينتوم جروث، شركة سعودية متخصصة في تطوير الأعمال والتسويق بالعمولة والشراكات التجارية وربط الكفاءات بفرص التوظيف."':
 'content="Momentum Growth is a Saudi company specialising in business development, consulting, commission-based marketing, commercial partnerships and connecting talent with employment."',
'content="مومينتوم جروث | Momentum Growth"': 'content="Momentum Growth"',
'content="الزخم الصح يصنع النمو. شريكك في تطوير الأعمال والتسويق والشراكات في المملكة العربية السعودية."':
 'content="The right momentum creates growth. Your partner for business development, marketing and partnerships in Saudi Arabia."',
'content="https://momentumgrowth.com.sa/"': 'content="https://momentumgrowth.com.sa/en/"',
# ---- nav ----
'<li><a href="#about">من نحن</a></li>': '<li><a href="#about">About</a></li>',
'<li><a href="#services">خدماتنا</a></li>': '<li><a href="#services">Services</a></li>',
'<li><a href="#sectors">القطاعات</a></li>': '<li><a href="#sectors">Sectors</a></li>',
'<li><a href="#models">نماذج التعاون</a></li>': '<li><a href="#models">How we partner</a></li>',
'<li><a href="#insights">رؤى</a></li>': '<li><a href="#insights">Insights</a></li>',
'<li><a href="#contact">تواصل معنا</a></li>': '<li><a href="#contact">Contact</a></li>',
'<li><a href="#process">منهجيتنا</a></li>': '<li><a href="#process">Approach</a></li>',
'<a class="nav-contact" href="#contact">تواصل معنا</a>': '<a class="nav-contact" href="#contact">Contact us</a>',
'<a class="lang" href="/en/" hreflang="en" lang="en">EN</a>': '<a class="lang" href="/" hreflang="ar" lang="ar">عربي</a>',
'aria-label="القائمة"': 'aria-label="Menu"',
# ---- hero ----
'<h1>الزخم الصح<br>يصنع <em>النمو</em></h1>': '<h1>The right momentum<br>creates <em>growth</em></h1>',
# ---- topics ----
'aria-label="مواضيع"': 'aria-label="Topics"',
'<span class="t">استكشف:</span>': '<span class="t">Explore:</span>',
'<a class="chip" href="#models">الدفع مقابل النتائج</a>': '<a class="chip" href="#models">Pay for results</a>',
'<a class="chip" href="#sectors">التعليم والتدريب</a>': '<a class="chip" href="#sectors">Education &amp; training</a>',
'<a class="chip" href="#services">ربط الكفاءات بالتوظيف</a>': '<a class="chip" href="#services">Talent placement</a>',
'<a class="chip" href="#services">التسويق بالعمولة</a>': '<a class="chip" href="#services">Commission marketing</a>',
'<a class="chip" href="#services">الشراكات التجارية</a>': '<a class="chip" href="#services">Partnerships</a>',
'<a class="chip" href="#insights">رؤى</a>': '<a class="chip" href="#insights">Insights</a>',
# ---- about ----
'<h2>من نحن</h2>': '<h2>About us</h2>',
'<p class="lead">مومينتوم جروث شركة سعودية تعمل شريكاً عملياً للمنشآت التي تبحث عن نمو حقيقي. نبدأ من أساس ثابت، نبني عليه حركة مستمرة، ثم نقيس النتيجة بأرقام واضحة.</p>':
 '<p class="lead">Momentum Growth is a Saudi company working as a practical partner for organisations that want real growth. We start from a solid base, build steady movement on it, then measure the result in clear numbers.</p>',
'<p class="lead" style="margin-top:14px">اسمنا يختصر طريقتنا: الزخم هو الحركة التي تحرّك الأشياء، والنمو هو ما ينتج عنها. نعمل بنموذج يربط أجرنا بنتائج شركائنا، فنجاحنا مرتبط بنجاحهم.</p>':
 '<p class="lead" style="margin-top:14px">Our name is our method: momentum is the movement that gets things going, and growth is what follows. Our fees are tied to our partners\' results, so our success depends on theirs.</p>',
'<div class="value"><strong>واثق</strong><span>نتكلم بوضوح وبدون مبالغة</span></div>': '<div class="value"><strong>Confident</strong><span>We speak clearly, without exaggeration</span></div>',
'<div class="value"><strong>طموح</strong><span>نظرتنا دائماً للخطوة القادمة</span></div>': '<div class="value"><strong>Ambitious</strong><span>Always looking at the next step</span></div>',
'<div class="value"><strong>احترافي</strong><span>دقيقة في الشكل والمحتوى</span></div>': '<div class="value"><strong>Professional</strong><span>Precise in form and substance</span></div>',
'<div class="value"><strong>عملي</strong><span>نركّز على النتائج الملموسة</span></div>': '<div class="value"><strong>Practical</strong><span>Focused on tangible results</span></div>',
'<h3>بطاقة الشركة</h3>': '<h3>Company profile</h3>',
'<li><span>الاسم التجاري</span><span>شركة مومينتوم جروث</span></li>': '<li><span>Trade name</span><span>Momentum Growth Company</span></li>',
'<li><span>الاسم بالإنجليزية</span><span class="en">Momentum Growth Company</span></li>': '<li><span>Arabic name</span><span lang="ar">شركة مومينتوم جروث</span></li>',
'<li><span>الكيان القانوني</span><span>شركة ذات مسؤولية محدودة</span></li>': '<li><span>Legal form</span><span>Limited liability company</span></li>',
'<li><span>تاريخ التأسيس</span><span>11 يونيو 2026</span></li>': '<li><span>Founded</span><span>11 June 2026</span></li>',
'<li><span>المقر الرئيسي</span><span>المدينة المنورة</span></li>': '<li><span>Headquarters</span><span>Madinah, Saudi Arabia</span></li>',
# ---- services ----
'<h2>خدماتنا</h2>': '<h2>Our services</h2>',
'<p class="lead">خمس خدمات واضحة، من الاستشارة وفتح الأسواق إلى الشراكات والتسويق وربط الكفاءات بالفرص.</p>':
 '<p class="lead">Five clear services, from consulting and market entry to partnerships, marketing and connecting talent with opportunity.</p>',
'<h3>الاستشارات</h3>': '<h3>Consulting</h3>',
'<p>نقدّم استشارات عملية في تطوير الأعمال والتسويق والشراكات، مبنية على فهم السوق السعودي لا على قوالب جاهزة، وتنتهي بخطة تنفيذ لا بتقرير.</p>':
 '<p>Practical advice on business development, marketing and partnerships, built on knowledge of the Saudi market rather than templates, and ending in an execution plan rather than a report.</p>',
'<h3>تطوير الأعمال وفتح الأسواق</h3>': '<h3>Business development &amp; market entry</h3>',
'<p>ندرس السوق ونحدد الفرص الأنسب لمنشأتك، ثم نبني خطة دخول واضحة بأهداف قابلة للقياس.</p>':
 '<p>We study the market, identify the right opportunities for your organisation and build a clear entry plan with measurable targets.</p>',
'<h3>الشراكات التجارية</h3>': '<h3>Commercial partnerships</h3>',
'<p>نربطك بالشركاء والجهات المناسبة ونتولى التنسيق والمتابعة حتى تتحول الشراكة إلى تعاون فعلي.</p>':
 '<p>We connect you with the right partners and institutions and handle coordination and follow-up until the partnership becomes real cooperation.</p>',
'<h3>التسويق بالعمولة</h3>': '<h3>Commission-based marketing</h3>',
'<p>نسوّق خدماتك ومنتجاتك بنموذج مبني على النتيجة، وندير الحملات ونرفع تقارير دورية بالأرقام، فلا تدفع إلا مقابل ما يتحقق فعلاً.</p>':
 '<p>We market your services and products on a results-based model, run the campaigns and report periodically in numbers, so you only pay for what is actually achieved.</p>',
'<h3>ربط الكفاءات بفرص التوظيف</h3>': '<h3>Talent placement</h3>',
'<p>نعمل مع الجهات التعليمية والتدريبية ومنشآت القطاع الخاص لربط الخريجين والمتدربين بوظائف فعلية ومتابعة التوظيف حتى إتمامه.</p>':
 '<p>We work with education and training providers and private-sector employers to place graduates and trainees in real jobs, following each hire through to completion.</p>',
# ---- sectors ----
'<h2>القطاعات التي نخدمها</h2>': '<h2>Sectors we serve</h2>',
'<p class="lead">نعمل مع الشركات الكبرى والمنشآت الصغيرة والمتوسطة على حد سواء، ونركّز على القطاعات التي نفهم تفاصيلها.</p>':
 '<p class="lead">We work with large enterprises and SMEs alike, and focus on the sectors whose details we understand.</p>',
'<h3>الشركات الكبرى</h3><p>شركات ومجموعات تريد شريكاً محلياً يفتح لها قطاعاً جديداً أو يدير لها قناة شراكات وتوظيف بمسؤولية كاملة.</p>':
 '<h3>Large enterprises</h3><p>Companies and groups that want a local partner to open a new sector or run a partnerships and recruitment channel with full accountability.</p>',
'<h3>المنشآت الصغيرة والمتوسطة</h3><p>منشآت تريد فتح أسواق جديدة أو قنوات بيع إضافية دون توظيف فريق تسويق كامل.</p>':
 '<h3>Small &amp; medium enterprises</h3><p>Businesses that want new markets or additional sales channels without hiring a full marketing team.</p>',
'<h3>التعليم والتدريب</h3><p>معاهد وأكاديميات ومراكز تدريب تبحث عن طلاب جدد ووظائف لخريجيها.</p>':
 '<h3>Education &amp; training</h3><p>Institutes, academies and training centres looking for new students and jobs for their graduates.</p>',
'<h3>الخدمات والمنتجات الاستهلاكية</h3><p>علامات تجارية تريد توسيع انتشارها عبر شراكات ووكلاء بنموذج عمولة واضح.</p>':
 '<h3>Consumer services &amp; products</h3><p>Brands that want wider reach through partners and agents on a clear commission model.</p>',
# ---- process ----
'<h2>منهجيتنا</h2>': '<h2>How we work</h2>',
'<p class="lead">أربع خطوات ثابتة نطبقها في كل مشروع، مهما اختلف حجمه أو قطاعه.</p>': '<p class="lead">Four fixed steps we apply to every engagement, whatever its size or sector.</p>',
'<p>«أساس ثابت، ثم حركة مستمرة، ثم نمو واضح يتجاوز نقطة البداية.»</p>': '<p>“A solid base, then steady movement, then clear growth beyond the starting point.”</p>',
'<div><h3>الفهم</h3><p>نجلس معك لنفهم منشأتك وسوقك وما الذي يعنيه النمو بالنسبة لك تحديداً.</p></div>': '<div><h3>Understand</h3><p>We sit with you to understand your organisation, your market and what growth specifically means to you.</p></div>',
'<div><h3>الخطة</h3><p>نضع خطة عمل بأهداف رقمية ومدد زمنية ومسؤوليات واضحة لكل طرف.</p></div>': '<div><h3>Plan</h3><p>We set a work plan with numeric targets, timelines and clear responsibilities for each side.</p></div>',
'<div><h3>التنفيذ</h3><p>ننفذ بأنفسنا ونتابع يومياً، ونعدّل المسار متى ما أظهرت الأرقام حاجة لذلك.</p></div>': '<div><h3>Execute</h3><p>We do the work ourselves, follow up daily and adjust course whenever the numbers call for it.</p></div>',
'<div><h3>القياس</h3><p>نرفع تقارير دورية معتمدة بالمستندات، ونحاسب أنفسنا على النتيجة لا على الجهد.</p></div>': '<div><h3>Measure</h3><p>We deliver periodic, documented reports and hold ourselves to results, not effort.</p></div>',
# ---- models ----
'<h2>نماذج التعاون</h2>': '<h2>How we partner</h2>',
'<p class="lead">ثلاثة نماذج واضحة، تختار منها ما يناسب هدفك. في كلها لا تدفع مقدماً مقابل وعود.</p>': '<p class="lead">Three clear models. Pick the one that fits your goal. In none of them do you pay upfront for promises.</p>',
'<h3>التسويق بالعمولة</h3>\n        <p class="fit"><b>يناسب:</b> منشأة لديها خدمة أو منتج جاهز وتريد عملاء أكثر.</p>': '<h3>Commission-based marketing</h3>\n        <p class="fit"><b>Best for:</b> an organisation with a ready service or product that wants more customers.</p>',
'<li>نتفق على تعريف دقيق للعميل المستهدف وسعر العمولة.</li>': '<li>We agree a precise definition of the target customer and the commission rate.</li>',
'<li>نسوّق عبر قنواتنا وشبكة علاقاتنا.</li>': '<li>We market through our channels and network.</li>',
'<li>نسلّمك كشفاً شهرياً بالعملاء الفعليين.</li>': '<li>You receive a monthly statement of actual customers.</li>',
'<div class="pay">المقابل: عمولة عن كل عميل يتم التعاقد معه فعلاً</div>': '<div class="pay">Fee: a commission on every customer actually signed</div>',
'<h3>التوظيف مقابل النتيجة</h3>\n        <p class="fit"><b>يناسب:</b> جهة تعليمية أو تدريبية تريد توظيف خريجيها، أو منشأة تبحث عن كفاءات.</p>': '<h3>Results-based recruitment</h3>\n        <p class="fit"><b>Best for:</b> an education or training provider that wants its graduates employed, or an employer looking for talent.</p>',
'<li>نستلم بيانات المرشحين ونصنّفها حسب التخصص.</li>': '<li>We receive candidate data and classify it by specialisation.</li>',
'<li>نتواصل مع منشآت القطاع الخاص ونرتب المقابلات.</li>': '<li>We approach private-sector employers and arrange interviews.</li>',
'<li>نتابع حتى التسجيل الرسمي في التأمينات الاجتماعية.</li>': '<li>We follow up until official registration with social insurance (GOSI).</li>',
'<div class="pay">المقابل: مبلغ ثابت عن كل توظيف مُوثّق</div>': '<div class="pay">Fee: a fixed amount per documented hire</div>',
'<h3>الشراكة التجارية</h3>\n        <p class="fit"><b>يناسب:</b> منشأة تريد دخول سوق أو قطاع جديد وتحتاج شريكاً محلياً.</p>': '<h3>Commercial partnership</h3>\n        <p class="fit"><b>Best for:</b> an organisation entering a new market or sector that needs a local partner.</p>',
'<li>ندرس السوق ونحدد الجهات والشركاء المحتملين.</li>': '<li>We study the market and identify potential partners and institutions.</li>',
'<li>نفتح الباب ونفاوض ونرتب الاتفاقيات.</li>': '<li>We open doors, negotiate and arrange the agreements.</li>',
'<li>نبقى طرفاً مسؤولاً عن المتابعة بعد التوقيع.</li>': '<li>We remain accountable for follow-up after signature.</li>',
'<div class="pay">المقابل: نسبة من الإيراد الناتج عن الشراكة</div>': '<div class="pay">Fee: a share of the revenue the partnership generates</div>',
# ---- why ----
'<h2>لماذا مومينتوم جروث</h2>': '<h2>Why Momentum Growth</h2>',
'<p class="lead">لأننا نعمل بنموذج يجعل مصلحتنا ومصلحتك في اتجاه واحد.</p>': '<p class="lead">Because our model points our interests and yours in the same direction.</p>',
'<h3>الدفع مقابل النتائج</h3><p>نعمل بعقود مبنية على العمولة والإنجاز الفعلي، لا على الوعود.</p>': '<h3>Pay for results</h3><p>Our contracts are built on commission and actual delivery, not promises.</p>',
'<h3>شفافية كاملة</h3><p>كشوفات دورية معتمدة ومرفقة بالمستندات، تعرف منها كل ما تحقق.</p>': '<h3>Full transparency</h3><p>Periodic, documented statements that show you exactly what was achieved.</p>',
'<h3>التزام بالأنظمة</h3><p>شركة مرخصة ومسجلة ضريبياً، وتلتزم بالأنظمة المرعية في المملكة في التسويق والتوظيف.</p>': '<h3>Regulatory compliance</h3><p>A licensed, tax-registered company that follows the Kingdom\'s marketing and employment regulations.</p>',
'<h3>قرب وسرعة استجابة</h3><p>فريق صغير ومباشر، تتعامل مع من يتخذ القرار، لا مع طبقات من الوسطاء.</p>': '<h3>Close and responsive</h3><p>A small, direct team. You deal with the decision-maker, not layers of intermediaries.</p>',
# ---- insights ----
'<h2>رؤى</h2>': '<h2>Insights</h2>',
'<p class="lead">قراءات قصيرة من واقع عملنا في السوق السعودي. نكتب ما نراه، بلا مبالغة.</p>': '<p class="lead">Short reads from our work in the Saudi market. We write what we see, without exaggeration.</p>',
'<h3>لماذا يناسب نموذج الدفع مقابل النتائج المنشآت الصغيرة والمتوسطة؟</h3>': '<h3>Why pay-for-results suits small and medium enterprises</h3>',
'<p>أغلب المنشآت الصغيرة لا تخسر بسبب ضعف منتجها، بل بسبب إنفاق تسويقي مقدّم لا يعود بشيء.</p>': '<p>Most small businesses do not fail because of a weak product, but because of upfront marketing spend that returns nothing.</p>',
'<summary>اقرأ المقال</summary>': '<summary>Read the article</summary>',
'<p>المنشأة الصغيرة تعيش على التدفق النقدي. عندما تدفع عقداً تسويقياً مقدماً ثم تنتظر النتيجة، تكون قد حوّلت المخاطرة كلها إلى جانبها. نموذج الدفع مقابل النتائج يقلب المعادلة: لا تدفع إلا عن عميل تعاقد فعلاً أو موظف سُجّل فعلاً.</p>':
 '<p>A small business lives on cash flow. When it pays for a marketing contract upfront and then waits for results, it has taken on all the risk itself. Pay-for-results flips the equation: you pay only for a customer who actually signed or an employee who was actually registered.</p>',
'<p>الفائدة الثانية أقل وضوحاً لكنها أهم: الشريك الذي يأخذ أجره من النتيجة يختار العملاء بعناية، ويرفض الوعود التي لا يستطيع تحقيقها. وهذا بالضبط ما يحتاجه صاحب المنشأة الذي لا يملك وقتاً لمراقبة كل حملة.</p>':
 '<p>The second benefit is less obvious but more important: a partner paid on results chooses clients carefully and refuses promises it cannot keep. That is exactly what an owner who has no time to monitor every campaign needs.</p>',
'<p>الشرط الوحيد لنجاح هذا النموذج هو تعريف "النتيجة" كتابةً قبل البدء: من هو العميل المقبول، وما المستند الذي يثبت التوظيف، ومتى يُستحق المقابل. بدون هذا التعريف يتحول النموذج إلى خلاف.</p>':
 '<p>The one condition for this model to work is defining “the result” in writing before starting: who counts as an acceptable customer, which document proves a hire, and when the fee is due. Without that definition the model turns into a dispute.</p>',
'<p class="meta">فريق مومينتوم جروث · 2026</p>': '<p class="meta">Momentum Growth team · 2026</p>',
'<h3>ما الذي تحتاجه الجهات التدريبية لتوظيف خريجيها فعلاً؟</h3>': '<h3>What training providers really need to get their graduates hired</h3>',
'<p>الشهادة وحدها لا توظّف. ما يوظّف هو شخص يعرف المنشآت ويتابع المرشح حتى يوم التسجيل في التأمينات.</p>': '<p>A certificate alone does not get anyone hired. What does is a person who knows the employers and follows the candidate through to the day of social-insurance registration.</p>',
'<p>كثير من المعاهد والأكاديميات تعد طلابها بالتوظيف، ثم تكتشف أن إدارة التوظيف عمل مختلف تماماً عن التدريب: يحتاج قاعدة بيانات منشآت، وعلاقات مع مسؤولي التوظيف، ومتابعة يومية للمقابلات، وتوثيقاً دقيقاً لكل حالة.</p>':
 '<p>Many institutes and academies promise their students employment, then discover that running placements is a completely different job from training: it needs an employer database, relationships with hiring managers, daily interview follow-up and precise documentation of every case.</p>',
'<p>الحل العملي أن تبقى الجهة التدريبية متخصصة فيما تجيده، وتسند التوظيف لشريك يعمل بمقابل عن كل توظيف موثّق. بهذا يصبح للشريك مصلحة مباشرة في أن يُوظَّف الطالب فعلاً، لا أن يُرشَّح فقط.</p>':
 '<p>The practical answer is for the training provider to stay focused on what it does well and hand placement to a partner paid per documented hire. The partner then has a direct interest in the student actually being employed, not merely nominated.</p>',
'<p>المعيار الذي ننصح به لأي جهة تدريبية: لا تعتمد أي توظيف إلا بإثبات تسجيل في التأمينات الاجتماعية، ولا تدفع عن توظيف يقل عمره عن المدة المتفق عليها. هذان الشرطان يحميان الطرفين.</p>':
 '<p>The standard we recommend to any training provider: accept no hire without proof of social-insurance registration, and pay for no hire shorter than the agreed period. Those two conditions protect both sides.</p>',
'<h3>كيف تختار شريكاً تجارياً لا يكلّفك أكثر مما يجلب؟</h3>': '<h3>How to choose a commercial partner that brings more than it costs</h3>',
'<p>الشراكة الجيدة تُعرف من عقدها لا من عرضها التقديمي. ثلاثة بنود تكشف كل شيء.</p>': '<p>A good partnership shows in its contract, not its pitch deck. Three clauses reveal everything.</p>',
'<p>البند الأول: كيف يُحسب أجر الشريك؟ إن كان مبلغاً ثابتاً مقدماً فالشريك لا يشاركك المخاطرة. وإن كان نسبة من النتيجة فمصلحتكما في اتجاه واحد.</p>':
 '<p>First: how is the partner paid? A fixed upfront amount means the partner shares none of your risk. A share of the result means your interests point the same way.</p>',
'<p>البند الثاني: ما الذي يلتزم به الشريك كتابةً؟ عدد الاجتماعات، التقارير الدورية، والمستندات المؤيدة لكل نتيجة. الشريك الجاد لا يمانع في تحديد هذه الالتزامات، بل يطلبها.</p>':
 '<p>Second: what does the partner commit to in writing? Number of meetings, periodic reports and supporting documents for every result. A serious partner does not resist these commitments; it asks for them.</p>',
'<p>البند الثالث: كيف تنتهي الشراكة؟ شرط إنهاء واضح بإشعار محدد يحمي الطرفين ويجعل أي خلاف مستقبلي محدود الأثر. غياب هذا الشرط هو السبب الأول في تحول الشراكات إلى نزاعات.</p>':
 '<p>Third: how does the partnership end? A clear termination clause with a defined notice period protects both sides and limits the impact of any future disagreement. Its absence is the leading reason partnerships turn into disputes.</p>',
# ---- contact ----
'<h2>تواصل معنا</h2>': '<h2>Contact us</h2>',
'<p class="lead">أخبرنا عن منشأتك وما تطمح إليه، وسنعود إليك خلال يوم عمل.</p>': '<p class="lead">Tell us about your organisation and what you are aiming for. We reply within one business day.</p>',
'<div><strong>المقر</strong><span>المدينة المنورة، المملكة العربية السعودية</span></div>': '<div><strong>Location</strong><span>Madinah, Kingdom of Saudi Arabia</span></div>',
'<strong>البريد الإلكتروني</strong>': '<strong>Email</strong>',
'<strong>الهاتف</strong>': '<strong>Phone</strong>',
'<div><strong>ساعات العمل</strong><span>الأحد إلى الخميس، 9 صباحاً إلى 5 مساءً</span></div>': '<div><strong>Working hours</strong><span>Sunday to Thursday, 9am to 5pm</span></div>',
'<h3>أرسل طلبك</h3>': '<h3>Send a request</h3>',
'<label for="name">الاسم</label>': '<label for="name">Name</label>',
'placeholder="الاسم الكامل"': 'placeholder="Full name"',
'<label for="company">المنشأة</label>': '<label for="company">Organisation</label>',
'placeholder="اسم المنشأة"': 'placeholder="Organisation name"',
'<label for="email">البريد الإلكتروني</label>': '<label for="email">Email</label>',
'<label for="phone">الجوال</label>': '<label for="phone">Mobile</label>',
'<label for="service">الخدمة المطلوبة</label>': '<label for="service">Service</label>',
'<option>الاستشارات</option>': '<option>Consulting</option>',
'<option>تطوير الأعمال وفتح الأسواق</option>': '<option>Business development &amp; market entry</option>',
'<option>الشراكات التجارية</option>': '<option>Commercial partnerships</option>',
'<option>التسويق بالعمولة</option>': '<option>Commission-based marketing</option>',
'<option>ربط الكفاءات بفرص التوظيف</option>': '<option>Talent placement</option>',
'<option>أخرى</option>': '<option>Other</option>',
'<label for="message">رسالتك</label>': '<label for="message">Message</label>',
'placeholder="أخبرنا باختصار عن منشأتك وما تحتاجه"': 'placeholder="Briefly tell us about your organisation and what you need"',
'<button class="btn btn-gold" type="submit">إرسال الطلب</button>': '<button class="btn btn-gold" type="submit">Send request</button>',
'<small>بالضغط على إرسال سيُفتح برنامج البريد لديك برسالة جاهزة إلى فريقنا.</small>': '<small>Clicking send opens your email app with a ready message to our team.</small>',
# ---- footer ----
'<p>شركة سعودية تعمل في تطوير الأعمال والتسويق والشراكات وربط الكفاءات بفرص التوظيف.</p>': '<p>A Saudi company working in business development, marketing, partnerships and talent placement.</p>',
'<h4>روابط</h4>': '<h4>Links</h4>',
'<li><a href="#about">من نحن</a></li>\n          <li><a href="#services">خدماتنا</a></li>': '<li><a href="#about">About</a></li>\n          <li><a href="#services">Services</a></li>',
'<li><a href="#sectors">القطاعات</a></li>\n          <li><a href="#models">نماذج التعاون</a></li>\n          <li><a href="#insights">رؤى</a></li>\n          <li><a href="#contact">تواصل معنا</a></li>': '<li><a href="#sectors">Sectors</a></li>\n          <li><a href="#models">How we partner</a></li>\n          <li><a href="#insights">Insights</a></li>\n          <li><a href="#contact">Contact</a></li>',
'<h4>بيانات رسمية</h4>': '<h4>Company</h4>',
'<li>شركة ذات مسؤولية محدودة</li>': '<li>Limited liability company</li>',
'<li>مسجلة لدى هيئة الزكاة والضريبة والجمارك</li>': '<li>Registered with the Zakat, Tax and Customs Authority</li>',
'<span>© 2026 شركة مومينتوم جروث. جميع الحقوق محفوظة.</span>': '<span>© 2026 Momentum Growth Company. All rights reserved.</span>',
# ---- scripts ----
"alert('الرجاء إدخال الاسم والبريد الإلكتروني.')": "alert('Please enter your name and email.')",
"'الاسم: '+f.name.value,'المنشأة: '+f.company.value,'البريد: '+f.email.value,'الجوال: '+f.phone.value,": "'Name: '+f.name.value,'Organisation: '+f.company.value,'Email: '+f.email.value,'Mobile: '+f.phone.value,",
"'الخدمة: '+f.service.value,'','الرسالة:',f.message.value": "'Service: '+f.service.value,'','Message:',f.message.value",
"encodeURIComponent('طلب تواصل من الموقع - '+f.name.value)": "encodeURIComponent('Website enquiry - '+f.name.value)",
# ---- alt text ----
'alt="شعار مومينتوم جروث"': 'alt="Momentum Growth logo"',
# ---- extra ----
'<strong>واتساب</strong>': '<strong>WhatsApp</strong>',
'<p class="fit"><b>يناسب:</b> منشأة لديها خدمة أو منتج جاهز وتريد عملاء أكثر.</p>': '<p class="fit"><b>Best for:</b> an organisation with a ready service or product that wants more customers.</p>',
'<h3>التسويق بالعمولة</h3>': '<h3>Commission-based marketing</h3>',
'<a class="btn btn-gold" href="#contact">تواصل معنا': '<a class="btn btn-gold" href="#contact">Contact us',
'<a class="btn btn-outline" href="#services">استعرض خدماتنا</a>': '<a class="btn btn-outline" href="#services">Our services</a>',
'<div><strong>شركة ذات مسؤولية محدودة</strong><span>مرخصة في المملكة العربية السعودية</span></div>': '<div><strong>Limited liability company</strong><span>Licensed in Saudi Arabia</span></div>',
'<div><strong>مسجّلة في ضريبة القيمة المضافة</strong><span>هيئة الزكاة والضريبة والجمارك</span></div>': '<div><strong>VAT registered</strong><span>Zakat, Tax and Customs Authority</span></div>',
'<div><strong>المدينة المنورة</strong><span>المملكة العربية السعودية</span></div>': '<div><strong>Madinah</strong><span>Kingdom of Saudi Arabia</span></div>',
}


missing = []
for k, v in T.items():
    if k in s:
        s = s.replace(k, v)
    else:
        missing.append(k[:60])

# asset paths one level up
s = s.replace('"assets/', '"../assets/').replace("url(\"assets/", "url(\"../assets/")

io.open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(s)

# report untranslated Arabic
left = [ (i+1, l.strip()[:90]) for i, l in enumerate(s.split('\n')) if re.search(r'[\u0600-\u06FF]', l) ]
print('missing keys:', len(missing))
for m in missing: print('  MISSING:', m)
print('arabic lines left:', len(left))
for n, l in left[:40]: print('  ', n, l)
