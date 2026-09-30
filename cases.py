"""
Case-study content — long-form narrative, one entry per project slug.

STRUCTURE (mirrors the reference case study, in the NK visual system)
    hero      headline + sub + meta (role / timeline / team)
    challenge lead + body[] + optional callout
    discovery lead + body[] + obs[] + findings[]        — omit with None
    insight   quote + body[]                            — omit with None
    solution  lead + body[] + decisions[]
    outcome   lead + body[]
    reflection title + body[]                           — omit with None

DELIBERATELY NO METRICS. Every number on a portfolio should be one you
can defend in an interview, so none are invented here. When you have
real figures, add a `metrics=[("13s", "Order processing", "2-3x faster")]`
key to any entry and the band will render itself.

IMAGES. Each `decisions[]` entry gets an image slot, and any files you
drop into  assets/projects/<slug>/  fill them in filename order
(01.jpg, 02.jpg …). Empty slots render as a quiet placeholder, so the
page is never broken while you're still collecting screens.
"""

# shared shorthand ---------------------------------------------------------
def C(lead, body, callout=None):
    return dict(lead=lead, body=body, callout=callout)


CASES = {

# ══════════════════════════════════════════════════════════ SEU · REGISTRY
"seu-admin": dict(
  headline="The other side of the same login: SEU Registry",
  sub="The staff console behind the student portal — one student record, thirty departments editing it.",
  role="Lead Product Designer", timeline="2024 — 2025",
  team="Product owner, engineering, registrar, quality assurance, HR and finance",

  challenge=C(
    "Every screen a student sees has a member of staff on the other end of it.",
    ["The student portal is the visible half of the system. The half that keeps it true is this one: a register where the university's whole student body lives, and where admissions, the registrar, quality assurance, HR, finance, the library and the chancellery all edit the same record for different reasons.",
     "That record is not small. One student carries personal and parental data, educational history, orders, a student card of every semester taken, credit recognition from a previous institution, mobility decisions, documents, contracts, statements, notices, insurance, research, logs and a diploma supplement.",
     "The failure mode of software like this is well known: each department gets its own screen, the same field is entered three times, and nobody can say which copy is correct."],
    ("Constraint", "One record, many editors",
     "The design problem was not making the data visible. It was making it obvious who owns which part of a record that a dozen roles can write to.")),

  discovery=None,
  insight=dict(
    quote="Administrative staff do not browse. They arrive with a student in mind and a decision to make about them.",
    body=["Nobody opens this system to look around. Somebody has come to the window, or an email has arrived, and a specific person's record has to be found, checked and changed within a couple of minutes.",
          "So the product is built around one shape: find the student, open the student, and everything the university knows about them is a list on the left. Whatever the department, the route is identical — which is what makes the system learnable by someone who only uses two of its thirty sections."]),

  solution=dict(
    lead="Find, open, and work down a single spine.",
    body=["The register is the front door: search by ID, filter, select, act in bulk, export. The columns are the ones staff actually identify a student by — ID, name, school, speciality, step, semester, status — not everything the database happens to hold.",
          "Opening a student replaces the page with a fixed identity header and a section rail. The header carries the facts that change how a case is handled — registration status, grant percentage, priority, refugee, medallist, underage — so a member of staff is never one click away from the context that should change their decision."],
    decisions=[
      ("A register built for finding one person",
       "Search, filter, bulk select, export — and columns staff recognise.",
       ["The table is sorted, paginated and exportable because half the requests that reach a registrar end in a spreadsheet for somebody else. Making export a first-class action removed a whole category of manual work.",
        "Row actions are limited to edit and detail. Everything more consequential happens inside the student, where the full context is on screen — bulk operations on a list are how records get damaged."]),
      ("The identity header never leaves",
       "Status, grant, priority, underage and the record's QR pinned above every section.",
       ["Thirty sections, one context. Whether a member of staff is editing insurance or a diploma supplement, they can see that this student is a minor, on a ninety-percent grant and currently registered — the flags that most often change what is allowed.",
        "Personal data itself is the longest form in the product, so it is broken into named blocks — name, personal, parental, contact, additional — rather than one column of fields. Verification and two-factor state sit at the end, where the record is confirmed rather than entered."]),
      ("Actions on the row they belong to",
       "Assign, transfer, inspect, edit, remove — at the end of each line.",
       ["A student's educational information is a set of enrolments, each with its own status, step and method of inclusion, and each needing a different action. Putting those actions on the row keeps a decision attached to the thing it is about.",
        "Destructive actions keep one colour and one position everywhere in the product, so the muscle memory of a daily user never lands on the wrong control."]),
      ("The academic record folded by semester",
       "One accordion per programme and season, with credits and GPA on the fold.",
       ["The student card is the document staff are asked about most, and it is naturally hierarchical: programme, then academic year and semester, then subjects with lecturer, credits, points and result. The summary a caller usually wants — credits taken and GPA — sits on the closed row.",
        "A student with more than one programme gets one block per programme rather than a merged list, because merging them is exactly the mistake the paper version used to make."]),
      ("Recognition shown as a comparison",
       "What was studied elsewhere on the left, what it counts for here on the right.",
       ["Credit recognition is an argument about equivalence, so the screen is built as two columns: the courses and credits a student brings, and the courses in this programme they are being mapped onto, with the totals resolved underneath.",
        "The alternative — two separate tables and a staff member holding the mapping in their head — is where recognition decisions actually go wrong."]),
      ("Status before detail",
       "External mobility, internal mobility and recognition as three states, not three forms.",
       ["Most of the time a member of staff only needs to know whether a process is finished. Three large cards answer that in one look, and the detail is one level down for the cases that are not.",
        "It also gives the section an honest empty state: a process that has not started reads as not started, rather than as an empty table that looks broken."]),
    ]),

  outcome=dict(
    lead="One record, one route to it, and a system a new hire can be shown in an afternoon.",
    body=["Admissions, the registrar, quality assurance, HR, finance, the library and the chancellery now work on the same student record through the same register, the same identity header and the same section rail.",
          "Because the staff console and the student portal are two views of one system, what a student sees in their account is what the registrar sees in theirs — which removes the reconciliation work that used to sit between them."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Internal software is judged by how it behaves on a bad day: a queue at the window, a deadline, a record that is not quite right. Almost every decision here was made for that day rather than for the demo.",
          "The lesson I keep from it is that consistency is a feature in administrative tools in a way it is not elsewhere. Thirty sections that behave identically are worth more than five sections individually optimised."]),
),


# ══════════════════════════════════════════════════════════ SEU · STUDENT
"seu-student": dict(
  headline="Registration week, without the queue: SEU Student",
  sub="The student's side of the university — enrolment, credits, library and surveys behind one login.",
  role="Lead Product Designer", timeline="2024 — 2025",
  team="Product owner, engineering, registrar, library and quality assurance",

  challenge=C(
    "A university runs on a handful of rules, and the student is the last person to be told what they are.",
    ["Course registration is the sharpest example. A student has a credit ceiling for the semester, a programme that divides those credits between compulsory, elective and research components, prerequisites that silently disqualify half the catalogue, and a registration window that opens at a fixed hour and closes when the groups fill.",
     "Before the portal, all of that lived in the registrar's office: printed programme sheets, a queue in a corridor, and a member of staff doing arithmetic on the student's behalf. Everyone involved was doing manual work that the rules could do themselves.",
     "The rest of the account had the same shape. Books, contracts, surveys, decrees, finances and the timetable each had their own custodian, their own form, and no single place where a student could see their own standing."],
    ("Constraint", "Everything happens in one week",
     "Registration is not steady traffic. The entire student body arrives inside a few hours, mostly on a phone, mostly anxious, and mostly making a decision they cannot easily undo. That is the load the interface has to be designed for.")),

  discovery=None,
  insight=dict(
    quote="Students were not asking for more information. They were asking whether they were allowed to press the button.",
    body=["Every question at the registrar's window reduced to one of three: how many credits do I still have, am I eligible for this course, and did my choice actually save.",
          "So the portal answers those three continuously rather than on request. The credit budget sits in the header on every tab, eligibility is attached to each row rather than buried in a regulation, and every selection resolves to a visible state instead of a silent success."]),

  solution=dict(
    lead="One account, one table, and the rules stated where the decision is made.",
    body=["The student card at the top carries identity and standing together — programme, status, semester, GPA, credits selected against the credit limit — and it does not move when you change tabs. Registration is a budgeting exercise, so the budget is always on screen.",
          "Underneath it, everything a student does with courses is the same table seen through different filters: their own programme, free credits, concentration, history, what they have already chosen, and the exchange market for swapping a group. Learning the table once is enough to use all six."],
    decisions=[
      ("The credit budget is a fixed frame, not a screen",
       "Selected against limit, visible on every tab.",
       ["Twenty-one of thirty is the only number that matters during registration, and it changes with every click. Keeping it in the header — outside the tabs, above the scroll — means a student never has to leave what they are doing to find out where they stand.",
        "The programme components carry the same idea one level down: each block shows what it requires against what has been chosen, so an under-filled research component is visible before the window closes rather than after."]),
      ("Eligibility on the row, not in the regulations",
       "Prerequisites next to the course, and a plain list of what was committed to.",
       ["Each course states its own prerequisite in plain text beside it, and a flag marks the rows a student cannot take yet. The alternative — a rule published somewhere else — makes the student the integration layer between a PDF and a form.",
        "The action follows the same logic: an eligible course offers Select, an already-chosen one offers removal, and nothing offers an action it will refuse to complete. Selected courses then repeats back the timetable a student has actually built — day, hour, room, professor — because a registration confirmed only as a credit total is not a confirmation."]),
      ("Group exchange as a market, not a request form",
       "My groups on the left, requirements on the right.",
       ["Timetable clashes are usually solved by two students who each want what the other has. Splitting the screen into what you hold and what you have asked for turns a support ticket into a transaction the students can settle themselves.",
        "The empty state matters more than the full one here: most students open this tab with nothing pending, so it has to explain what the tab is for rather than look broken."]),
      ("History that stays folded until asked",
       "One collapsed row per season, expanding into the full record.",
       ["A master's student accumulates a dozen semesters of groups, professors and grades. Presented as one long table it is unreadable; presented as seasons it is a list of eight things, any of which opens into detail.",
        "The same accordion carries the programme components on the registration tab, so expansion means the same thing everywhere in the product."]),
      ("The library is a catalogue with a shelf attached",
       "Catalogue, my books, reserved and returned — one table, four states.",
       ["A book is either available, on your shelf, waiting for you, or back with the library. Those are states of one record rather than four separate features, so they are four tabs over the same columns and the same search.",
        "The full bibliographic record — contents, ISBN, UDC, publisher, pages — opens in a side panel rather than a new page, because a student comparing three books should not lose the list to look at one of them."]),
      ("Surveys asked one page at a time",
       "A stack of cards, a scale that reads left to right, and a visible 1 / 4.",
       ["Institutional evaluation only produces useful data if students finish it. Showing the whole questionnaire at once guarantees they will not, so it is dealt in pages with the remaining depth visible behind the current card.",
        "Every scale keeps the same direction and the same 'hard to answer' escape, so a student who disengages leaves a gap rather than a random answer."]),
    ]),

  outcome=dict(
    lead="The registrar's desk, moved into the student's account.",
    body=["Registration, course exchange, academic history, the library, institutional surveys, documents, contracts, finances and notices now sit behind one login, sharing one navigation and one set of table and state patterns.",
          "The work that used to be a queue at a counter is now a decision a student makes for themselves, inside the constraints of their own programme, with the rules visible at the point where they apply."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Administrative software is mostly the transcription of rules, and the temptation is to transcribe them into help text. Nearly everything good here came from moving a rule onto the object it constrains — the credit ceiling into the header, the prerequisite onto the row, the deadline into the notification.",
          "The part I would push harder on is the empty and error states. 'Progress will be lost' and 'the programme does not provide for a concentration' are the moments a student is most likely to give up, and they deserved as much attention as the tables did."]),
),


# ══════════════════════════════════════════════════════════ SEU
"seu": dict(
  headline="Leading it rather than drawing it: SEU",
  sub="The site for Georgian National University SEU — where the design problem was mostly a question of who gets to decide.",
  role="Design Lead", timeline="2024 — 2025", team="UI designer, engineering, marketing, faculty stakeholders",
  live="https://seu.edu.ge/ka",

  challenge=C(
    "A university website is not one product. It is a dozen departments sharing one address.",
    ["Admissions wants applicants. Faculties want their programmes visible. Research wants publications. Career services, the library, the tech centre, international relations, the affiliated hospital — each arrives with a legitimate claim on the homepage and a page count of their own.",
     "The audiences are just as split. A Georgian school-leaver comparing universities, an Indian student choosing where to study medicine, a current student looking for the academic calendar, and a partner institution checking credibility all need different first screens.",
     "Left unmanaged, that produces the familiar result: a site that is an org chart with a header on it, navigable by whoever already knows the structure."],
    ("Opportunity", "The structure is the deliverable",
     "On a site this size, the information architecture and the rules that protect it outlast every visual decision. Get that right and the interface has something to be consistent about.")),

  discovery=None,
  insight=dict(
    quote="My job here was not to draw the screens. It was to make sure the screens that got drawn were answering the same question.",
    body=["I led this one rather than executing it — a UI designer did the interface work, with engineering, marketing and faculty stakeholders alongside. That changes what the work actually is.",
          "Most of my hours went to deciding what the site is for, whose need wins when two departments want the same slot, and what the standard is — then reviewing against that standard rather than against taste. A designer who is given a clear rule produces better work than one who is given a redline."]),

  solution=dict(
    lead="Audience-led entry points on top of a departmental structure.",
    body=["The top of the site addresses people by why they came — applicants, faculties, international relations, the MIT and EHL partnerships — while the full departmental tree stays available underneath for those who know what they are looking for.",
          "The partnerships get the prominence they earn: for a Georgian university competing for students, an MIT or EHL affiliation is the strongest available proof, so it leads rather than sitting in an about page."],
    decisions=[
      ("Entry by audience, not by department",
       "Applicants, faculties, international, partnerships across the top.",
       ["Nobody arrives thinking 'I need the Industrial Collaboration and Career Development Department'. They arrive as a school-leaver or a parent or a prospective partner, and the first row of the site says so in those terms."]),
      ("One structure, held",
       "A published pattern for section, listing and article — and a review against it.",
       ["The value of a lead on a project this size is refusing exceptions. Every department has a reason why theirs is special; a written structure turns that from a negotiation into a decision that was already made."]),
      ("Proof over adjectives",
       "MIT, EHL, GWU, the affiliated hospital, named students.",
       ["Universities describe themselves in superlatives that all sound identical. Named partners, real student testimony and the campus itself do the persuading that the copy cannot."]),
      ("A news stream that does not swamp the site",
       "Announcements and news given their own rhythm.",
       ["A university publishes constantly — conferences, competitions, deadlines. Containing that flow in its own patterns keeps the permanent content from being pushed under it every week."]),
    ]),

  outcome=dict(
    lead="A site the university can keep adding to.",
    body=["SEU runs at seu.edu.ge in Georgian and English, covering admissions, faculties, research, student life and the international partnerships, with a continuous announcements and news stream on top.",
          "New programmes, partners and departments drop into the existing patterns — which was the point of spending the time on structure rather than on screens."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["This is the clearest example I have of design leadership being a different job from design. I did not produce the UI here, and the project was better for it — my contribution was the brief, the structure, the standard and the review.",
          "The hardest part was not visual. It was telling a department that their section would not lead the homepage, and having a reason good enough that the answer held."]),
),


# ══════════════════════════════════════════════════════════ IOKA
"ioka": dict(
  headline="One catalogue, two buyers: IOKA",
  sub="A Dubai property portal where half the visitors want somewhere to live and half want somewhere to put money.",
  role="UX/UI Designer", timeline="2025", team="Founders, brokers, engineering",
  live="https://ioka.ae/",

  challenge=C(
    "The same listing has to answer two questions that barely overlap.",
    ["Someone relocating to Dubai wants to picture a life: the light in the room, the walk to the beach, the school. Someone buying the identical apartment as an asset wants yield, payment plan, handover date and how quickly it can be resold.",
     "Most property sites pick one of those and quietly fail the other. Dubai cannot — off-plan investment and residential search sit in the same catalogue, and a broker's whole business is being credible to both.",
     "There is also a stranger problem underneath: a large share of the inventory does not exist yet. Off-plan means the buyer is committing to a render, a floor plan and a completion date."],
    ("Opportunity", "Intent is the first filter, not price",
     "Off-plan, resale and rental are not categories of property. They are three different reasons for being on the site, and asking that first makes every screen after it simpler.")),

  discovery=None,
  insight=dict(
    quote="Nobody is browsing. They arrive already knowing whether this is a home or a position.",
    body=["That is why the intent switch sits above the search fields rather than inside the filters. Choosing off-plan, resale or rental changes what the rest of the form should even ask — a rental shopper does not care about payment plans, an investor does not care about move-in dates.",
          "It also resolves the tone problem. The same photograph can be sold as a lifestyle or as an asset; deciding which one the visitor came for means the page no longer has to do both at once."]),

  solution=dict(
    lead="Intent first, then inventory, then proof.",
    body=["The search opens on a three-way switch and only then asks where, how big and how much. Listings inherit that context, so an off-plan card leads with handover and payment structure while a rental card leads with availability.",
          "Because much of the stock is unbuilt, the page has to earn trust it cannot demonstrate. That work is done by who is standing behind the deal: named developers, named team, real reviews."],
    decisions=[
      ("Off-plan, resale, rental as the first choice",
       "The reason for visiting, asked before any property is shown.",
       ["Three intents, one control, at the top of the fold. Everything downstream — fields, card content, sort order — is derived from it, which keeps a catalogue of tens of thousands navigable without a filter panel."]),
      ("Areas, not an endless list",
       "Dubai is bought by district, so the district is the browse unit.",
       ["Buyers here talk in place names — Palm Jumeirah, Dubai Hills, JVT — long before they talk in bedrooms. Leading with area cards matches how the decision is actually narrowed and gives the imagery room to work."]),
      ("Developer names doing the credibility",
       "Emaar, Sobha, DAMAC, Binghatti, Aldar in their own right.",
       ["When the product is a building that does not exist, the developer's reputation is the product guarantee. Their marks are given real estate on the page rather than being hidden in a footer strip."]),
      ("A named team, not a contact form",
       "Founders and brokers with faces, tenure and reviews.",
       ["A first-time overseas buyer is wiring a deposit to a company they found on Instagram. Showing who they would be dealing with does more for conversion than any amount of interface polish."]),
    ]),

  outcome=dict(
    lead="A portal that sorts people before it sorts property.",
    body=["IOKA runs at ioka.ae as the agency's storefront across off-plan, resale and rental, alongside the blog that carries the market analysis the investor audience arrives for.",
          "The structure has absorbed a growing catalogue and a widening developer roster without the navigation needing to change."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["The instinct on a listings product is to build a better filter panel. The more useful move was one question above the fold, because it made most of the filtering unnecessary.",
          "The other lesson was about trust as a design material rather than a content afterthought. On a catalogue of buildings that are still renders, the team page and the developer logos are load-bearing — they are doing the job the product photography cannot."]),
),


# ══════════════════════════════════════════════════════ SYNIOTEC · SAM
"syniotec-sam": dict(
  headline="A machine with nobody certified to drive it is not a resource: Syniotec SAM",
  sub="The construction-company platform \u2014 projects, equipment, personnel, crews, warehouses, dispatch and workshop \u2014 for firms whose plan falls apart when one of those is missing.",
  role="Senior UX/UI Designer", timeline="Jul 2021 — present",
  team="2 PM, 4 developers, field ops",

  challenge=C(
    "Construction software is normally sold as one of two products, and a construction company needs both at once.",
    ["Fleet tools plan machines. Workforce tools plan people. A site foreman needs an excavator, a driver with a valid ticket for it, a transport to get it there and a slot in the calendar when all three are free — and the moment any one of those is planned separately, the plan is fiction.",
     "SAM covers projects, requests, crews, equipment, warehouses, personnel, dispatch and workshop. Eight objects, six departments, all editing the same week.",
     "It also has to read machines it did not sell. Cross-manufacturer telematics and the AEMP 2.0 standard mean the platform ingests data from competitors' hardware, at whatever quality that hardware happens to report."],
    ("Opportunity", "Make the crew the unit of planning",
     "Every competitor plans a machine or a person. Planning them as one object is the whole product, and it is a design decision before it is an engineering one.")),

  discovery=None,
  insight=dict(
    quote="Nobody schedules an excavator. They schedule an excavator, a driver who is allowed to operate it, and a lorry to move it.",
    body=["Asking which of those the software is for is the wrong question, and it is the question the market had been answering for years.",
          "So the planning surface takes equipment and personnel in the same action, and crews \u2014 whose types the customer defines themselves \u2014 become the thing assigned to a project. Qualifications stop being an HR record and become a scheduling constraint, which is what they always were on site."]),

  solution=dict(
    lead="Two views, one calendar and one map, over eight objects that plan together.",
    body=["Everything in SAM resolves to time or place, so the calendar and the map are the two lenses that repeat across projects, equipment and personnel rather than being features of any one of them. A project is a location with a duration; a machine is a position with a schedule; an employee is availability with certificates attached.",
          "Around that sit the flows the office actually runs on: a request from site that carries a status from ask to approval, a transport that dispatch either gives to an internal driver or offers to a haulier, an inspection completed on a phone, and a cost-centre allocation that hands the machine's hours to the billing system."],
    decisions=[
      ("Equipment and people planned in one action",
       "Crews as the assignable unit, with customer-defined crew types.",
       ["Planning them separately produces a schedule that only works if somebody in the office remembers who is qualified for what. Making the crew the object moves that knowledge into the system, where it can be checked.",
        "Crew types are defined by the customer rather than by us, because a road-building crew and a pipeline crew are different shapes and any fixed template would be wrong for most of the market."]),
      ("Qualifications are a planning constraint",
       "Certificates, expiry and status sit in the scheduling view.",
       ["A certificate that expires next month is a scheduling fact, not a personnel file. Surfacing it where the assignment is made stops the class of mistake that only becomes visible when an inspector arrives.",
        "The same view carries absence and holiday, so availability is one answer rather than three systems agreeing by accident."]),
      ("A request is an object, not a phone call",
       "Site asks for a machine, equipment or people; the ask carries its own status.",
       ["The demand for a resource used to exist only as a conversation, which meant it could not be queued, prioritised or measured. Giving the request an identity and a state \u2014 from raised to approved \u2014 is what turns coordination into something the platform can help with.",
        "It also gives the site a way to see where their ask has got to, which removes most of the follow-up calls that generated the original chaos."]),
      ("Calendar and map, everywhere",
       "The same two lenses over projects, equipment and personnel.",
       ["Construction has two dimensions that matter: when and where. Building those as universal views rather than per-module features means a user learns them once and reads every part of the product with them.",
        "Geofences hang off the same map \u2014 a project or a warehouse gets a boundary, and a machine leaving it raises an alarm. Security stops being a separate product and becomes a property of a place already drawn."]),
      ("Built to read other manufacturers' machines",
       "Cross-vendor telematics and AEMP 2.0 rather than our own hardware only.",
       ["A fleet is bought over twenty years from a dozen suppliers. A platform that only reads its own devices asks a customer to re-equip before they can start, which is not a request anybody grants.",
        "Designing for uneven data is the consequence: a machine reporting only position has to sit legibly beside one reporting hours, fuel and fault codes, without the sparse one looking broken."]),
      ("Inspections signed where they happen",
       "VDBUM protocols on a phone, with photographs and a signature, stored as PDF.",
       ["A technical inspection is a compliance artefact that has to survive years and an auditor. Completing it on the machine, with the photographs taken there and the examiner's signature attached, is the difference between a record and a reconstruction.",
        "Filing it back into the equipment profile as a PDF means the proof lives with the asset rather than in somebody's folder."]),
    ]),

  outcome=dict(
    lead="One platform where the plan includes the people.",
    body=["SAM runs projects, equipment, personnel, crews, warehouses, dispatch and workshop for construction firms from Bremen outwards \u2014 including operations at the scale of STRABAG \u2014 with a mobile client for the half of the workforce that is never at a desk.",
          "The design system built alongside it is why six modules and eight object types still read as one product: states, density and the calendar-and-map pairing were decided once and inherited everywhere."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["The valuable insight was not a screen. It was noticing that the industry had split a single question \u2014 can this job happen on Tuesday \u2014 into two products, and that joining them back together was worth more than improving either half.",
          "The harder discipline was refusing to design for our own hardware. Every time the interface assumed rich telematics, it quietly excluded the customer with a mixed twenty-year-old fleet, which is most of the market."]),
),

# ══════════════════════════════════════════════════════ HALYK BANK
"halyk-bank": dict(
  headline="Opening a deposit without phoning the branch: Halyk Bank Georgia",
  sub="A UX pass over the internet bank\u2019s deposit flow \u2014 the product a customer only uses when they are about to hand over money.",
  role="UX/UI Designer", timeline="2021", team="Bank product team, engineering",

  challenge=C(
    "Opening a deposit online is a small flow with an unusually high cost of doubt.",
    ["The customer is choosing between products that differ in ways banks find obvious and customers do not \u2014 term, rate, whether you can top it up, what happens if you withdraw early. Three options with similar names and different consequences.",
     "It also has a legal spine. Terms have to be presented, mandatory fields have to be filled, and the confirmation has to be unambiguous, because what is being agreed is a contract rather than a purchase.",
     "And the fallback is always available: if the screen is confusing for thirty seconds, the customer calls the branch, and the digital channel has failed at the only moment it was supposed to save anybody time."],
    ("Opportunity", "Make the comparison, not just the form",
     "The hard part is not entering the amount. It is knowing which of the three deposits is the right one \u2014 and that decision was happening on the phone, not on the screen.")),

  discovery=None,
  insight=dict(
    quote="Nobody abandons a form because it is long. They abandon it because they are no longer sure they are doing the right thing.",
    body=["Every drop-off in this flow traced back to a moment of uncertainty rather than a moment of effort \u2014 which product, what the terms mean, whether this is reversible.",
          "So the work went into the deciding rather than the filling in: the three products presented so they can be compared, the terms readable where the decision is made, and a confirmation that restates what is about to happen."]),

  solution=dict(
    lead="Compare, agree, confirm \u2014 in that order, with no step doing two jobs.",
    body=["The three deposit types are presented side by side on their differences rather than their names, so the choice is made once and the rest of the flow inherits it. Terms and conditions are readable at the point of selection instead of behind a checkbox at the end.",
          "The rest is a short form of genuinely mandatory fields, a review screen that restates the deposit in plain language, and a notification when it is open. Afterwards the deposit appears in the account dashboard with its balance and interest earned, because a product you cannot see is a product you will phone about."],
    decisions=[
      ("Compare on the difference, not the name",
       "Three deposits shown side by side on term, rate and access.",
       ["Product names carry meaning inside a bank and none outside it. Laying the three out against the attributes that actually differ turns a naming problem into a reading problem.",
        "Doing this before the form means the customer commits once. Every later screen can then be about completion rather than reconsideration."]),
      ("Terms where the decision is",
       "Readable at selection, not hidden behind a final checkbox.",
       ["Presenting terms at the end guarantees they are agreed rather than read, and it puts the least comfortable moment immediately before the commitment.",
        "Moving them next to the product turns them into part of the comparison \u2014 which is what they are."]),
      ("A confirmation that says it back",
       "Amount, term, rate and date restated before submission.",
       ["The last screen before a financial commitment should contain no new information and no new decisions. Restating the deposit in plain language is what lets somebody press the button without hesitating.",
        "A notification on completion closes the loop, and the deposit appearing in the dashboard afterwards is what keeps the customer from calling to check it worked."]),
    ]),

  outcome=dict(
    lead="A deposit opened on a screen instead of at a counter.",
    body=["The flow works on phone, tablet and desktop, and the deposit is visible and manageable afterwards \u2014 balance, interest, terms \u2014 without contacting the bank.",
          "The change that carried the most weight was moving the product comparison before the form, which is a structural decision rather than a visual one."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Banking flows are usually optimised for fewer fields. This one needed fewer doubts, which is a different problem and often means adding content rather than removing it.",
          "The measure I would use again: not how long the flow takes, but at which step somebody would reach for the phone."]),
),

# ══════════════════════════════════════════════════════ DEUTSCHE BANK
"deutsche-bank": dict(
  headline="A chart language for people who read hundreds a day: Deutsche Bank",
  sub="Chart and dashboard design for financial data analysis \u2014 consolidating datasets into views an analyst can read, compare and share.",
  role="UX/UI Designer", timeline="2021", team="Client product team",

  challenge=C(
    "An analyst does not look at a chart. They look at forty, and only two of them matter.",
    ["Financial data arrives from several sources in several shapes, and the job is to get it into one consolidated view fast enough that the analysis happens the same day the question was asked.",
     "At that volume, every decorative decision becomes a tax. A gradient, a drop shadow or a needless legend costs nothing on one chart and costs real time across a screen of twenty.",
     "And the output is rarely for the person who made it. A chart is built to be sent \u2014 into a meeting, a report, a decision \u2014 so it has to carry its meaning without the analyst standing next to it."],
    ("Opportunity", "Design the set, not the chart",
     "Consistency across the whole family is worth more than the quality of any single visualisation, because the reader is comparing rather than admiring.")),

  discovery=None,
  insight=dict(
    quote="The value is not in what the chart shows. It is in how quickly you can rule it out.",
    body=["Most charts an analyst opens are not the answer. The job of the visual language is to make that judgement in a second, so attention lands on the two that matter.",
          "That points everything at legibility and consistency: same axis treatment, same density, same colour meaning, so nothing has to be re-learned chart to chart."]),

  solution=dict(
    lead="One visual grammar across every chart type.",
    body=["Bar, line, scatter and their relatives share axis behaviour, label density, grid weight and a palette in which colour always means the same thing. Data comes in from CSV, Excel, JSON or a live source; the platform cleans and organises it so the analyst is choosing a view rather than preparing a file.",
          "Customisation is deliberately narrow \u2014 palette, type, data labels \u2014 and annotations sit on the chart itself, so the interpretation travels with the data into whatever meeting it ends up in."],
    decisions=[
      ("Colour means one thing everywhere",
       "A fixed palette with fixed semantics across the whole family.",
       ["When colour is chosen per chart, the reader has to check the legend every time. Fixing it across the set turns colour into something you read rather than decode.",
        "It also survives the real destination of these images \u2014 a slide, a printout, a screenshot in a message \u2014 where the legend often does not travel with them."]),
      ("Density tuned for a screen of charts",
       "Grid weight, label frequency and margins set for twenty at once.",
       ["Every chart was reviewed at the size it appears in a dashboard rather than at full width, because that is where the analyst actually meets it.",
        "Gridlines and labels are the first things to thin out at small sizes; getting that threshold right is most of the difference between a readable dashboard and a wall of ink."]),
      ("Annotation is part of the chart",
       "Notes and comments attached to the data, not written around it.",
       ["A chart sent without its interpretation gets interpreted anyway, usually wrongly. Letting the analyst attach the reasoning to the point it refers to is what turns a visualisation into an argument.",
        "Real-time sources mean the chart stays current after it is shared, so the annotation and the data do not drift apart."]),
    ]),

  outcome=dict(
    lead="A set of charts that behave like one system.",
    body=["Analysts assemble consolidated views from multiple sources, read them at dashboard density, and share them with the interpretation attached.",
          "The gain is cumulative rather than dramatic: nothing has to be re-read, because everything behaves the same way."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Data visualisation work is judged on the showpiece chart and lived through the boring ones. Designing the axis and the label rules properly was worth more than any individual view.",
          "The other lesson is that restraint here is not taste, it is throughput. Every removed ornament is time returned to somebody reading their fortieth chart of the day."]),
),

# ══════════════════════════════════════════════════════ NEURO PILOT
"neuro-pilot": dict(
  headline="A virtual psychologist has to be careful about what it claims: Neuro Pilot",
  sub="A Georgian-language mental wellbeing app \u2014 psychoeducation, self-assessment questionnaires and guided exercises, in a language that had almost none of them.",
  role="Product Designer", timeline="2023", team="Founders, psychologists, mobile developers",

  challenge=C(
    "The product calls itself a virtual psychologist. Most of the design work was deciding what that is not allowed to mean.",
    ["An app that asks about anxiety, self-worth and how you handle failure is asking clinical questions. It is not a clinician, and the distance between those two things has to be visible in the interface rather than buried in a terms page.",
     "The audience made it harder rather than easier. Georgian has very little of this material \u2014 few apps, few translated instruments, and a culture where talking to a psychologist still carries some weight. For many users this would be the first structured thing they had ever read about their own thinking.",
     "And the content is long. Cognitive behavioural material is explanatory by nature: several paragraphs before a single question is worth asking. On a phone, that is the hardest kind of content to hold someone through."],
    ("Constraint", "First contact, not clinical care",
     "The realistic best outcome is that someone learns a little, recognises something in themselves, and \u2014 where it matters \u2014 goes and talks to a professional. The interface had to be designed for that outcome rather than for retention.")),

  discovery=None,
  insight=dict(
    quote="Teach first, then ask. A question you do not understand does not measure anything.",
    body=["Screening instruments assume the person answering knows what is being asked and why. Drop those questions on someone cold and you get noise \u2014 politeness, guessing, and the answer they think is correct.",
          "So every questionnaire in the app is preceded by the explanation it depends on: what the pattern is, why it matters, what the exercise will do about it. The teaching is not context around the test; it is the reason the test means anything."]),

  solution=dict(
    lead="A guided sequence \u2014 read, answer, practise \u2014 with the limits of the product stated in the copy.",
    body=["The app opens as what it is: NEUROPILOT, a virtual psychologist, in Georgian, with three onboarding cards and one action. Sign-up offers a free account, Google or Apple, with the language switch in the corner because the whole product is written for one market.",
          "From there each module follows the same shape: an illustrated explanation, one questionnaire, and a practice session with audio. The visual language \u2014 warm cream, deep purple, flat editorial illustration \u2014 was chosen to sit as far as possible from anything clinical."],
    decisions=[
      ("The name is a promise, so it is stated plainly",
       "NEUROPILOT \u2014 \u10d5\u10d8\u10e0\u10e2\u10e3\u10d0\u10da\u10e3\u10e0\u10d8 \u10e4\u10e1\u10d8\u10e5\u10dd\u10da\u10dd\u10d2\u10d8, and nothing more implied.",
       ["Calling a product a virtual psychologist sets an expectation in one word. The onboarding does not embellish it \u2014 three cards, a subtitle, an illustration and a single button, so the promise stays the size it can actually deliver.",
        "The illustration system does the reassuring instead of the copy. A paper plane and a node graph are friendly and abstract; a brain scan or a couch would have made a claim the product cannot support."]),
      ("A greeting that sets the conditions",
       "Name, a short orientation, and the headphone prompt before anything begins.",
       ["The session opens by addressing the person by name and telling them how to sit with it \u2014 headphones on if possible, muted if not. Audio-guided exercises fail quietly when someone starts them on a train with the sound off, so the requirement is stated before the first module rather than discovered halfway through.",
        "The mute control then stays available on every screen that carries audio. Consistency here is a trust matter: a wellbeing app that surprises you with sound has broken something more important than a preference."]),
      ("Two kinds of question, and the interface says which",
       "\u201cSelect one or more\u201d and \u201conly one answer\u201d, written above the options.",
       ["Multi-select and single-select look nearly identical on a phone and mean completely different things to the instrument underneath. Stating the rule in words above the list \u2014 rather than trusting a circle to imply it \u2014 removes the most common way a self-assessment gets answered wrongly.",
        "Options are full-width rows with the target spanning the whole card, because the answers themselves are long sentences about uncomfortable feelings and should not be reached for through a small circle at the edge of the screen."]),
      ("The explanation carries the weight, not the result",
       "Several paragraphs before the exercise, and a footnote about the time it takes.",
       ["Each module explains the pattern it addresses \u2014 replacing failure scenarios with a different way of thinking \u2014 in plain language before asking anyone to practise it. This is the longest text in the product and the part that earns everything after it.",
        "A quiet footnote states how long the programme takes and when results become available. Setting the pace explicitly is what stops the app being judged as a thing that did not work overnight."]),
      ("A result that says what it is not",
       "\u10e2\u10d4\u10e1\u10e2\u10d8\u10e1 \u10de\u10d0\u10e1\u10e3\u10ee\u10d8 \u2014 framed as a general indication, not a diagnosis.",
       ["The answer screen states that the information gathered is for general assessment \u2014 of anxiety, low mood and self-perception \u2014 rather than a finding about the person. That sentence is the most important copy in the product and it is on the screen, not in a policy.",
        "It also sets up the only honest escalation an app like this has: noticing something is useful, and acting on it usually means talking to somebody qualified."]),
    ]),

  outcome=dict(
    lead="Structured psychological material, in Georgian, on a phone.",
    body=["The app delivers cognitive behavioural content as a sequence a person can actually finish \u2014 explanation, self-assessment, guided practice \u2014 in a language where almost none of this existed in app form.",
          "The patterns that carried the most weight were the least visual ones: stating the question type, stating the audio requirement, stating the time it takes, and stating what a result is not."]),

  reflection=dict(
    title="What I would keep, and what I would revisit",
    body=["Two visual directions were explored \u2014 a light one built around a 3D brain, and the warm cream-and-purple editorial direction that shipped. The second won because the first looked medical, and looking medical is a claim.",
          "What I would revisit is the placeholder copy that survived into the onboarding cards. Lorem-ipsum jokes in a product about anxiety are a small thing that says the wrong thing, and the first screen is where a nervous user decides whether to trust the rest."]),
),

# ══════════════════════════════════════════════════════ HALYK ATM
"halyk-open-banking": dict(
  headline="Letting a rival bank read your accounts: Halyk Open Banking",
  sub="The consent portal where a Halyk customer grants another bank access to their own data \u2014 by scope, by account and by currency.",
  role="UX/UI Designer", timeline="2022", team="Bank product team, compliance, engineering",

  challenge=C(
    "Open banking asks an ordinary person to make a permissions decision that IT departments find difficult.",
    ["A competitor \u2014 named, in this case TBC \u2014 is requesting access to somebody\u2019s Halyk accounts so that inter-bank transfers and aggregated balances work. Regulation says the customer must consent, specifically and revocably.",
     "\u2018Specifically\u2019 is the hard word. Access to balances is not access to transaction history, and neither is access to account details; and a customer with three accounts in three currencies is looking at nine possible grants per scope.",
     "Get it wrong in one direction and the screen is a wall of checkboxes nobody reads before clicking through. Get it wrong in the other and it is a single Allow button that gives away everything and satisfies the letter of the rule while defeating its purpose."],
    ("Constraint", "Consent has to be readable and specific at the same time",
     "Those pull against each other, and the resolution is structure rather than fewer options.")),

  discovery=None,
  insight=dict(
    quote="A person cannot reason about nine permissions. They can reason about three questions asked three times.",
    body=["The grid is only overwhelming when it is presented as one flat list. Split by what is being asked for \u2014 balances, transactions, account details \u2014 and each block becomes a single comprehensible question with a familiar answer set underneath it.",
          "Every level then gets its own select-all, so the trusting customer is one tap and the careful one still has every individual choice available. Nobody is forced through nine decisions to reach the common case."]),

  solution=dict(
    lead="Three scopes, each with its own accounts, each with its own shortcut.",
    body=["The requesting institution is named in the sentence at the top, in quotation marks, as a legal entity rather than as \u2018an application\u2019. Beneath it, three cards \u2014 balances, transactions, account details \u2014 each listing every IBAN and currency the customer holds, each with an all-accounts control, and a select-everything at the very top for people who already decided before they arrived.",
          "Nothing is pre-ticked. The terms are a link next to a separate checkbox, and the green consent button stays inert until an actual choice has been made."],
    decisions=[
      ("Name the bank that is asking",
       "\u2018SS \u201cTBC Bank\u201d requests permission to access your accounts.\u2019",
       ["Consent screens habitually say \u2018a third party\u2019 or \u2018the application\u2019, which is precisely the information a person needs and the thing they are least likely to guess. The legal name in quotation marks is the whole sentence\u2019s work.",
        "Being explicit is also in Halyk\u2019s interest here. A customer who knows they are handing data to a competitor is making a real decision, and a real decision is the only kind that holds up later."]),
      ("Three scopes before three hundred checkboxes",
       "Balances, transactions and account details as separate blocks.",
       ["Grouping by what is being requested turns nine grants into three questions. A customer can refuse transaction history while allowing balances \u2014 which is exactly the granularity the regulation intends and the granularity a flat list destroys.",
        "Each block carries its own select-all, and the page carries one above them. The common answer is one tap; the careful answer is still fully available underneath."]),
      ("Two factors before a single account is shown",
       "Username, password, then an SMS code \u2014 and only then the list.",
       ["The portal never displays an IBAN to somebody who has not completed both steps, because the consent screen is itself an inventory of what the customer owns.",
        "The code field appears in place with a resend control beside it rather than on a new screen, so the second factor reads as part of signing in rather than as a separate obstacle."]),
    ]),

  outcome=dict(
    lead="Consent that is specific enough to be meaningful and short enough to be read.",
    body=["A Halyk customer can authorise another bank to see exactly what they choose \u2014 by scope, account and currency \u2014 from a portal that does one thing and then gets out of the way.",
          "The structure is what makes it work: three questions rather than one switch or one long list."]),

  reflection=dict(
    title="What I would change",
    body=["The promotional rail beside the consent panel is the part I would argue about again. A savings card and a \u2018switch from another bank\u2019 offer sitting next to a permission decision competes for the attention that decision needs, and on a screen with regulatory weight the commercial real estate is the first thing I would give up.",
          "The design lesson I would keep is that granularity and comprehension are not opposites. They only appear that way when the options are presented flat \u2014 the right grouping makes a long list short without removing a single choice."]),
),


"halyk-onboarding": dict(
  headline="Seven ways to already exist: Halyk Bank onboarding",
  sub="Registration for the Halyk Bank mobile app, where the design problem is not the form \u2014 it is what the state registry and the bank\u2019s own records say about you before you have finished typing.",
  role="UX/UI Designer", timeline="2021", team="Bank product team, compliance, engineering",

  challenge=C(
    "Onboarding a bank customer in Georgia means asking two databases about them, and neither one answers yes or no.",
    ["Three fields \u2014 personal number, date of birth, phone \u2014 and the app already knows more about you than you have typed. The national personal number reaches the Entrepreneurs\u2019 Registry; the phone reaches the bank\u2019s own customer records.",
     "Between them they produce a branch for every kind of person who might be standing there: a genuinely new customer, somebody already in the bank\u2019s database without an active account, somebody who already has internet banking, a business whose registry entry stops the process, and several ways for the lookup to simply fail.",
     "There is also a compliance layer that cannot be softened away. Legal form, tax residency, whether the applicant is a US taxpayer under FATCA, and a consent text that has to be shown in full \u2014 all of it before an account exists."],
    ("Constraint", "The happy path is the rare one",
     "Most onboarding is designed for the person who sails through. Here the branches were the majority of the screens, and the majority of the work.")),

  discovery=None,
  insight=dict(
    quote="Every one of these outcomes is a person standing there with a phone. \u2018Registration failed\u2019 tells them nothing about what to do next.",
    body=["An error state that only reports the system\u2019s condition puts the burden back on the customer, who then phones the branch \u2014 which is the exact cost the app existed to remove.",
          "So each branch was written as a situation rather than a status: what we found, what that means for you, and the one thing to do about it. That is why there are seven end screens instead of one."]),

  solution=dict(
    lead="Ask for almost nothing, then be honest about what came back.",
    body=["The form is three fields, and the phone number carries the country code because a Georgian bank knows where its customers are. A six-digit SMS code follows, with the number it was sent to shown on screen and a visible resend countdown \u2014 so waiting is a state rather than a silence.",
          "The regulatory questions sit behind segmented tabs that split an individual from a sole trader from a company, so nobody reads questions that do not apply to them. Then the lookups run, and whichever of the seven outcomes comes back gets its own screen with its own next step."],
    decisions=[
      ("Three fields, and one of them does the work",
       "Personal number, date of birth, phone \u2014 nothing else.",
       ["The national personal number is the key to everything the state already knows, so asking for a name, an address or a company would be asking somebody to type what the registry is about to return.",
        "The phone field carries +995 rather than a country picker. A dropdown of two hundred countries on a domestic bank\u2019s registration form is a decision nobody needs to make."]),
      ("Waiting is a state, not a silence",
       "The number shown, a countdown, and a numeric pad already open.",
       ["The SMS screen states which number the code went to, which is the only question anybody has at that moment, and counts down to when a resend becomes available instead of leaving the option greyed out with no explanation.",
        "The pad opens on arrival and the boxes advance on their own \u2014 six digits should be six taps and nothing else."]),
      ("Split the compliance questions by who is answering",
       "Individual, sole trader and company as segmented tabs.",
       ["Legal form, tax status and FATCA residency are three different conversations depending on which one you are. Putting them behind a segment means an individual never reads a question about a company\u2019s registration certificate.",
        "The questions themselves are asked as questions \u2014 are you a US tax resident, yes or no \u2014 rather than as the regulation they come from. The regulation is what the answer is for, not what the customer is here to understand."]),
      ("Consent shown in full, and scrollable",
       "The whole text, with the agreement below it.",
       ["A consent that is summarised is not a consent. The full text is on the screen and the accept control sits after it, so agreement follows reading rather than replacing it.",
        "The alternative \u2014 a checkbox next to a link \u2014 collects a tap and produces nothing anybody could defend later."]),
      ("Already existing is not an error",
       "Internet banking already active; in our records without an account.",
       ["Two of the most common outcomes are that the person is already known to the bank. Treating either as a failure sends an existing customer to a call centre to be told they are a customer.",
        "Each gets a screen that names the situation and offers the action that resolves it \u2014 sign in, or continue and activate \u2014 so the branch is a fork rather than a dead end."]),
      ("The registry can stop the process, and the screen says so",
       "What came back, what it means, and who to talk to.",
       ["Some registry answers genuinely end the flow: a legal form the app cannot open an account for, or a record that does not exist. Pretending otherwise wastes the customer\u2019s next ten minutes.",
        "So the terminal screens state the finding plainly and route the person to the one channel that can help, which is the honest version of a dead end and the only one that does not generate a complaint."]),
    ]),

  outcome=dict(
    lead="An account opened from a phone, or a clear reason why not.",
    body=["Registration takes three fields and an SMS for the straightforward case, and every other case ends on a screen that names the situation and offers a next step rather than an error code.",
          "The success screen lists what actually happened \u2014 the account, the mobile banking access, the confirmation \u2014 because the last thing a new customer needs is to wonder whether it worked."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Onboarding portfolios are full of happy paths. This project was almost entirely the other thing, and it taught me that the branch screens are where a bank either keeps a customer or hands them to a call centre.",
          "The rule I took from it: an error state that only describes the system has not been designed. It has to describe the person\u2019s situation and give them one thing to do."]),
),


"halyk-cards": dict(
  headline="A card is the only piece of a bank people carry: Halyk Bank Georgia",
  sub="The physical card family — credit, debit, gold, platinum and business — for Halyk Bank\u2019s Georgian arm.",
  role="UX/UI Designer", timeline="2021", team="Bank product &amp; marketing team",
  shots="plain",

  challenge=C(
    "Every other thing a bank makes lives on a screen. This one lives in a wallet for three years.",
    ["A card has to do several jobs at once with almost no room: identify the bank in half a second, tell the holder which product they have, satisfy Visa and Mastercard\u2019s placement rules, survive a card printer, and still look like it belongs to the same family as the six cards beside it.",
     "It is also the most durable brand asset a bank owns. A campaign runs for a month; a card is handed over at a till hundreds of times over its life, usually face-up, usually next to somebody else\u2019s.",
     "And the constraints are unusually hard. Chip and contactless positions are fixed, network marks have minimum sizes and clear space, the magnetic stripe and signature panel own the back, and the printed data has to stay legible at a glance in bad light."],
    ("Opportunity", "The tier is the design problem",
     "Nothing else on the card can vary much. So the entire product ladder has to be carried by colour and by one word.")),

  discovery=None,
  insight=dict(
    quote="On a counter, the card is read at arm\u2019s length by someone who is not looking for information.",
    body=["That rules out most of what a designer would want to add. Pattern, texture and illustration all compete with the two things that have to survive that glance: whose bank it is and which card it is.",
          "So the family was built the other way around — strip the face to almost nothing, and let a single flat colour do the work of naming the tier."]),

  solution=dict(
    lead="One layout, six colours, and a back that earns its keep.",
    body=["Every card in the range shares an identical face: logo top-left, chip and contactless below it, network mark bottom-right, and the tier word in the opposite corner where nothing else competes with it. Change the colour and you have changed the product.",
          "The palette moves through the range rather than decorating it — sage for credit, the brand\u2019s teal for everyday debit, beige for gold, graphite for platinum and black for business. Nothing is metallic or gradient: flat colour prints predictably and ages better than an effect."],
    decisions=[
      ("The tier is a colour, not a badge",
       "Beige, graphite, black, sage and teal — one flat field each.",
       ["A customer holding two Halyk cards should be able to tell them apart in a wallet, in the dark, by edge alone. Colour does that at a distance no typography can reach.",
        "Flat rather than metallic was a production decision as much as an aesthetic one. Foils and gradients shift between print runs and scuff visibly within months; a solid field looks the same on the day it is issued and two years later."]),
      ("An empty face is a decision, not a shortage",
       "Logo, chip, contactless, network mark, one word. Nothing else.",
       ["The temptation on a card is to add a pattern to justify the design. Every element added is one more thing competing at the moment the card is read, which is a second at a counter.",
        "The tier word sits in the corner diagonally opposite the logo, so the two things that matter occupy the two positions the eye reaches first and last, with nothing in between."]),
      ("The numbers moved to the back",
       "Front kept clean; card number, holder and expiry printed on the reverse.",
       ["Putting the number on the back keeps the face uncluttered and makes the card marginally harder to read over a shoulder or in a photograph — a small, real privacy gain that costs nothing.",
        "The printed data uses a mono-spaced face so digits stay evenly spaced and legible in a mediocre print at a bad angle, which is how these are actually read."]),
      ("A QR code that does one job",
       "\u10d2\u10d0\u10d3\u10db\u10dd\u10ec\u10d4\u10e0\u10d4\u10d7 \u10e9\u10d5\u10d4\u10dc\u10d8 \u10db\u10dd\u10d1\u10d0\u10d8\u10da \u10d1\u10d0\u10dc\u10d9\u10d8 \u2014 download our mobile bank.",
       ["The one piece of real estate a bank never uses is the back of its own card. A QR code with a line of Georgian beside it turns three years in a wallet into a standing invitation to install the app.",
        "It is deliberately the only call to action anywhere on the card. A second one would make the back look like an advert, and a card that looks like an advert gets used less."]),
      ("Georgian first, on a Kazakh bank\u2019s card",
       "Georgian type on the reverse, and a Georgian app at the end of the QR.",
       ["Halyk is a Kazakh bank operating in Georgia, and the card is the most tangible proof of whether that is a local branch or a foreign object. The reverse is set in Georgian, and the QR beside it lands in an app that is also in Georgian \u2014 so the chain from wallet to phone never switches language.",
        "The Georgian script also had to sit comfortably beside a Latin logotype and a network mark — which is a type-pairing problem more than a layout one, and the reason the local line is set small and quiet rather than translated into a slogan."]),
    ]),

  outcome=dict(
    lead="A range that reads as one bank.",
    body=["The family covers Visa Credit, Visa Gold, Visa Platinum, Visa Business and Mastercard World Debit under a single layout, so a new product is a colour and a word rather than a new design.",
          "Because the face is almost empty, the constraint that usually breaks card design — network placement rules, chip position, print tolerances — stopped being something to work around and became the layout itself."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["This is the most constrained brief I have worked on and the one where restraint paid the most. There is nowhere to hide on a card: no scroll, no state, no second screen — every decision is visible at once, forever.",
          "The thing I would argue for again is the QR on the back. It is the only element that does work for the bank after issue, and it survived because it was the only one asking for attention."]),
),

# ══════════════════════════════════════════════════════ (remaining)
"syniotec-sam-mobile": dict(
  headline="A worker's day, not a fleet's database: SAM on mobile",
  sub="Syniotec's Software Asset Manager for the site — where the app has to start a shift, drive a delivery and book a machine into the workshop.",
  role="Senior UX/UI Designer", timeline="2022 — present",
  team="2 PM, 4 developers, field ops",

  challenge=C(
    "The desktop platform describes a fleet. The phone has to get somebody through a day.",
    ["SAM's original research found that field staff routed around the software because a phone call was faster. The desktop rebuild answered that for dispatchers and the office. It did not answer it for the person driving to Hamburg with a machine on the back.",
     "On site, asset management is not a category of software — it is a sequence of small obligations. Clock on. Find the excavator. Take it to a job. Confirm it arrived. Book it in for repair. Ask for Friday off.",
     "Every one of those was either a different system, a phone call, or a form somebody filled in at the end of the week from memory. The client's own line for the product says it best: less construction sites on construction sites."],
    ("Constraint", "Mixed literacy, mixed devices, one build",
     "The same app is opened by a mechanic, a driver, a workshop technician and a branch manager — some of them daily, some of them twice a month, on whatever phone they already own.")),

  discovery=None,
  insight=dict(
    quote="Nobody opens this app to manage assets. They open it to start their shift, or to prove they delivered something.",
    body=["That is why the home screen is a launcher rather than a dashboard. A dashboard assumes you came to look; a launcher assumes you came to do one specific thing and want it in two taps.",
          "It also settled what mobile owns. Equipment, transport, time and the workshop live here because they happen away from a desk. Anything that needs a keyboard stays on the platform."]),

  solution=dict(
    lead="A grid of jobs, not a menu of modules.",
    body=["The home screen is a set of large, named actions — look up equipment, add one, edit one, configure its telematics, move it, track time, send it to the Werkstatt — and the ones a given user cannot do are shown greyed rather than hidden.",
          "Underneath, each job is built for the moment it happens: a shift starts with one button, a delivery ends with one button, and a leave request sits beside the calendar it affects."],
    decisions=[
      ("A launcher, and it shows you the locked doors",
       "Every service as a large tile; unavailable ones greyed, not removed.",
       ["Icon-led tiles at that size survive a shared phone, a cracked screen and a user who opens the app twice a month. There is no navigation to learn — the whole product is visible on the first screen.",
        "Warehouse and Projects appear greyed out rather than hidden. Hiding what a role cannot reach makes people ask colleagues what they are missing; showing it disabled answers the question before it is asked and tells them the module exists."]),
      ("The shift is the first thing the app knows",
       "One button to start the day, and leave requests beside the calendar.",
       ["Time tracking opens on a single sentence — your shift starts in nine minutes — and one full-width action. Clocking on is the highest-frequency, lowest-thought interaction in the product, so it gets the largest target on the screen and no decisions attached to it.",
        "Vacation and sick days sit directly under it with their status in plain language, pending or approved, because the question a worker actually has is not 'where do I file this' but 'did anyone answer me'."]),
      ("A delivery ends with a button, not a form",
       "Live route, time remaining, ETA to the next stop, then confirm.",
       ["Transport is the part of the job done while moving, so the screen is a map with two facts on it — how long is left and when the next stop happens — and the confirmation is a single action at the bottom, reachable with a thumb.",
        "Confirming arrival where it happens is what makes the platform's timeline true. The alternative, which is what existed, is a driver reconstructing three drops from memory in the evening."]),
      ("Four tabs, and the workshop in the users' own words",
       "Home, Fleet, Projects, Crew — and Werkstatt stays Werkstatt.",
       ["The bottom bar names the four things the business is made of rather than the four biggest features, which keeps the structure stable as modules come and go.",
        "The client is a German operation and the workshop is called the Werkstatt on site, so it is called that in the interface. Translating vocabulary that a crew already shares buys nothing and costs recognition."]),
    ]),

  outcome=dict(
    lead="The record started being written where the work happens.",
    body=["Shifts, transports, workshop jobs and equipment changes are now entered on site instead of reconstructed later, which closes the gap the original research found: the platform used to be a few hours out of date exactly when accuracy mattered.",
          "Because the app shares the platform's tokens, states and component behaviour, it reads as the same product rather than a companion — a status in a driver's hand means what it means on a dispatcher's timeline."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["A field tool is not a small desktop tool. The temptation with a mature platform is to make it responsive and call that mobile, which produces something technically usable and practically ignored.",
          "The decision I would defend hardest is the greyed-out tiles. Every instinct says hide what the user cannot use; on a crew where people cover each other's roles, showing the whole product and locking part of it turned out to explain the system better than any onboarding would have."]),
),


"syniotec-ram-mobile": dict(
  headline="The rental fleet in a coat pocket: RAM on mobile",
  sub="Syniotec's Rental Asset Manager for the people on site — branch managers, mechanics and yard staff who need the fleet's state without opening a laptop.",
  role="Senior UX/UI Designer", timeline="2023 — present", team="Product, engineering",

  challenge=C(
    "The desktop module holds everything. The person on site needs four things from it.",
    ["On the web, RAM turned a forty-field booking into a sequence that matches how a dispatcher thinks. That solved the problem for the person with a keyboard.",
     "But a rental business is run across branches — Hamburg, Bremen, Berlin — by people who spend the day between a yard, a site and a van. They are not creating bookings from a phone; they are checking where the fleet stands, what is due today, and signing machines in and out at a gate.",
     "Those four jobs were spread across a platform designed for a large screen, and in practice they were being done by phone call, WhatsApp and paper docket."],
    ("Constraint", "Read far more often than written",
     "This is a client people open twenty times a day for ten seconds. Almost every session is a question, not an edit — so the design problem is answering fast, not capturing completely.")),

  discovery=None,
  insight=dict(
    quote="Porting the booking form would have been the obvious move and the wrong one.",
    body=["The complex part of RAM is genuinely complex and belongs on a desk. What was homeless were the simple parts — fleet status, today's tasks, and the physical handover of a machine.",
          "So the mobile client is not a smaller RAM. It is four objects — fleet, contracts, tasks, handover — each answerable in one screen, sharing the platform's data and its visual language."]),

  solution=dict(
    lead="Four objects in the tab bar, and a home screen that answers before you ask.",
    body=["Home opens on the state of the fleet rather than a menu: utilisation across working, maintenance and warehouse, the contract pipeline as preplanned, planned and in progress against a completed total, the tasks assigned to you, and a feed of what changed since you last looked.",
          "Everything below that is one level deep. Fleet holds equipment, technical checks and the telematics configurator; Contracts is a search; My Tasks is a list with a clock on it; and the handover protocols sit on the home screen itself, because signing a machine in or out is the thing most likely to happen while standing up."],
    decisions=[
      ("Home answers, it does not navigate",
       "Utilisation, pipeline, tasks and recent activity on one scroll.",
       ["A branch manager opening this app has one of about five questions, and every one of them is answered before a tap: how much of the fleet is earning, how much is in for maintenance, what is sitting in the warehouse, what is due today, and what has changed.",
        "The pipeline is shown as three rings against a total rather than a table of contracts. Preplanned, planned and in progress are states you check, not records you read — a shape is faster than a number, and the number is there underneath it anyway."]),
      ("Handover promoted to the home screen",
       "Hand in and hand out as two standing actions, not a buried flow.",
       ["Collection and return are where rental disputes are made or avoided, and they happen at a gate with a phone in one hand. Putting both protocols on the first screen means the record of an exchange is created at the moment of the exchange rather than reconstructed later.",
        "Two directions, named plainly. The asymmetry matters — handing a machine out is a condition check and a signature; taking one back is the same check read against what was recorded on the way out."]),
      ("Fleet is three jobs, not a database",
       "Equipment, technical checks and the IOT configurator.",
       ["The fleet tab could have been a searchable list of every asset. Instead it is the three things people do to a machine: look it up, inspect it, and configure what its telematics report.",
        "Keeping the configurator next to equipment rather than in a settings area reflects how it is actually used — you configure a sensor while standing in front of the machine it is bolted to."]),
      ("Tasks carry the client and the clock",
       "Project, customer, contract number and a due time on every row.",
       ["A task without a deadline is a note. Each row carries the project, the company it belongs to and the moment it is due, with the time treated as the most prominent thing on the line — because the only real question is whether it is today.",
        "The contract reference sits on the same row, so a task is one tap from the agreement it belongs to rather than a search away."]),
    ]),

  outcome=dict(
    lead="The branch fits on a phone.",
    body=["Fleet utilisation, the contract pipeline, the day's tasks and the physical handover of machines are now answered in seconds from a device people already have on them, across branches, without opening the desktop platform.",
          "The desktop module stays where complex bookings get built. Mobile owns the moments that were previously a phone call, a paper docket and a photo nobody could find."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Extending a mature platform to mobile is mostly an exercise in refusing to port things. The temptation is to make the powerful screens responsive; the value was in noticing which parts of the workflow were never difficult, only badly placed.",
          "The other thing I would keep is the ratio: this is a read-mostly product with two write actions on the front page, and being honest about that is what kept it to four tabs."]),
),


"syniotec-ram": dict(
  headline="Rental is won and lost at the gate: Syniotec RAM",
  sub="The rental platform \u2014 bookings, planning board, fleet, items, handovers and invoicing \u2014 for companies whose margin leaks in the two minutes a machine changes hands.",
  role="Senior UX/UI Designer", timeline="2022 — present", team="Product, engineering",

  challenge=C(
    "A rental company sells hours it cannot see and takes back machines it cannot inspect.",
    ["The contract says eight hours a day. The site runs twelve. Nobody counts, nobody invoices the difference, and the depot only finds out when the service interval arrives four months early.",
     "The other leak is the return. A machine comes back with a dent, an empty tank and a fortnight of argument about which of those was already there \u2014 settled, if at all, by whoever kept better notes.",
     "Around those two moments sits everything else: a planning board that has to show what is free and when, a catalogue holding both serialised machines and buckets of consumables, and an invoice that has to be right without anybody retyping the rental period."],
    ("Opportunity", "Design the two edges of the contract",
     "The middle of a rental is uneventful. The money is decided when the machine goes out, while it is running harder than agreed, and when it comes back.")),

  discovery=None,
  insight=dict(
    quote="Telematics does not make a rental company money. Noticing does.",
    body=["Every machine in the fleet was already reporting its hours. The gap was that the number sat in a report, and a report is something you look at after the quarter it would have helped.",
          "So overuse became a notification rather than a column \u2014 and the handover became a document the software produces rather than a form somebody is supposed to fill in."]),

  solution=dict(
    lead="A planning board for the day, and evidence at both ends of every rental.",
    body=["The planner is where a rental company actually lives: calendar and map side by side, availability visible, and drag-and-drop for the constant reshuffling that a week of bookings really is. Reservations hold a machine before it is contracted; the same board shows ongoing, planned and completed rentals without switching context.",
          "At the edges, handover protocols capture condition where the exchange happens, and operating hours feed straight into billing so an invoice is a consequence of the rental rather than a separate act of data entry."],
    decisions=[
      ("Overuse is an alert, not a column in a report",
       "Contracted hours against actual, with a notification when it slips.",
       ["Utilisation data is worthless if it is discovered late. Turning it into an automatic notice makes the difference between a conversation this week and a write-off next quarter.",
        "The same figure serves two purposes at once \u2014 it prices the overage and it warns the depot that a service is coming early. One number, read by two people who never speak."]),
      ("The handover protocol is the product's most valuable document",
       "Condition, photographs and a customer signature, captured at the gate.",
       ["Return disputes are the expensive failure in rental and they are decided entirely by what was recorded on the way out. Making the protocol something you complete at the machine rather than at a desk is what makes it evidence rather than recollection.",
        "It is sent to the customer for acceptance and signature and stored centrally, so the argument that used to be two people's memories becomes one document both of them agreed to."]),
      ("Let the model read the photograph",
       "Tank level, soiling and visible damage pulled from the handover images.",
       ["The person doing a handover is standing in a yard with a phone and a customer waiting. Every field they have to type is a field they will guess at, and a guessed field is not evidence.",
        "So the obvious readings \u2014 fuel, condition, damage \u2014 are proposed from the photographs and the operator confirms or corrects them. That is the right shape for this kind of model: it drafts, a human signs, and the human is the one whose name is on the document."]),
      ("Target against actual, on the customer's own project",
       "What was rented, compared with what the site needed.",
       ["Rental companies are usually blind to how their machines are being used once they leave. Comparing the booking against the customer's project turns the platform from a ledger into an account manager's argument for the next contract.",
        "It also surfaces the honest version of overuse: not a penalty to be charged, but a machine that was under-specified for the job."]),
      ("Two kinds of thing in one catalogue",
       "Serialised equipment with a profile; items without a serial number.",
       ["An excavator has an identity, telematics, a service history and a photograph. A box of blades has a price and a quantity. Forcing both into one record type makes one of them absurd.",
        "So items are a separate class that links to equipment, carries graduated price lists and joins the same rental contract \u2014 which is what lets an invoice cover the machine and everything that went out on the trailer with it."]),
      ("The invoice is a consequence",
       "Rental period and rates generate the billing information; ERP takes it from there.",
       ["Every hour retyped between the planner and the accounting system is an hour that can be typed wrong. Generating billing data from the rental itself removes the transcription rather than speeding it up.",
        "Open interfaces and AEMP 2.0 mean the figures land in whatever ERP the customer already runs, which is the only version of this that a twenty-year-old rental business will accept."]),
    ]),

  outcome=dict(
    lead="A rental fleet that reports what it earned and proves what condition it was in.",
    body=["RAM runs bookings, planning, fleet, items, handovers and invoicing for rental companies including Kurt K\u00f6nig and HOCH, with a mobile client for the yard \u2014 where the handovers actually happen.",
          "The two edges are where the design paid: hours that were previously invisible now bill, and condition that was previously argued now has a signature on it."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Finding the two moments that decide the money \u2014 and designing those first \u2014 was worth more than any improvement to the ninety per cent of the rental that is uneventful.",
          "The AI in the handover is also the shape I would repeat elsewhere. It reads what is tedious and obvious, proposes it, and stops. The signature stays human, because the document only has value if somebody is accountable for it."]),
),

"barclays-bank": dict(
  headline="Charts that survive being sent to someone else: Barclays",
  sub="A charting interface for bank employees \u2014 build a view from transaction, customer or market data, and share it without a designer in the loop.",
  role="UX/UI Designer", timeline="2021", team="Client product team",

  challenge=C(
    "The people who need the chart are not the people who can make one.",
    ["Inside a bank, the person with the question owns the data and has no visualisation skills; the person who can build a good chart is in another team with a queue. So the analysis either waits or gets done badly in a spreadsheet.",
     "The datasets are not interchangeable either. Transaction data, customer data and market data have different shapes, different sensitivities and different conventions for how they are read.",
     "And the chart is made to be circulated. Its real audience is a room of people who were not there when it was built."],
    ("Opportunity", "Make the default output presentable",
     "If an employee with no design training produces something publishable on the first try, the queue disappears.")),

  discovery=None,
  insight=dict(
    quote="Give a non-designer a colour picker and you have created work, not capability.",
    body=["Every configuration option in a tool like this is a chance to produce something worse than the default, and a decision the user did not want to make.",
          "So the templates carry the design, the data selection carries the meaning, and the customisation is limited to the handful of choices that are genuinely the user's to make."]),

  solution=dict(
    lead="Pick the data, pick the chart, send it.",
    body=["Employees sign in with existing credentials, choose from the datasets they are entitled to, and select a chart type that is already designed \u2014 sized, spaced and coloured to the bank's language before anything is touched.",
          "Filtering and sorting narrow the view, real-time sources keep it current, and sharing carries the chart with its annotations so the reasoning arrives with the picture."],
    decisions=[
      ("The template is the design work",
       "Chart types that are publishable before customisation.",
       ["The user's job is choosing the right data and the right chart type. Every visual decision below that \u2014 spacing, axis, label density, palette \u2014 was made once and applied everywhere.",
        "The narrow set of controls that remains is chosen so that no combination produces an unreadable result, which is the only way to give this to a whole bank."]),
      ("Sharing carries the reasoning",
       "Notes and comments travel with the chart.",
       ["A chart circulated inside a bank gets read by people who cannot ask a follow-up question. Attaching the interpretation to the data is what stops it being misread in the next meeting.",
        "Real-time connections mean the shared view does not quietly go stale, which is the usual failure of a screenshot pasted into a deck."]),
    ]),

  outcome=dict(
    lead="Analysis that does not queue.",
    body=["Employees build and circulate their own charts from the datasets they already have access to, without waiting on a design or reporting team.",
          "Because the design lives in the templates rather than in the user's hands, the output stays consistent no matter who made it."]),

  reflection=None,
),

"chat-bar": dict(
  headline="You are not meeting a stranger, you are meeting a bar: Chat Bar",
  sub="A location-based social app where the unit is the venue \u2014 check in, see who else is there, and start a conversation that already has a place attached to it.",
  role="Product Designer", timeline="2022", team="Founders, engineering",

  challenge=C(
    "Meeting people nearby is a safety problem long before it is a matching problem.",
    ["The obvious version of this app is a map of people around you. That version is also the one nobody sensible installs \u2014 broadcasting your live position to strangers is a cost no amount of social upside pays for.",
     "The second problem is the opening move. Talking to somebody in a bar is hard because there is nothing to talk about yet; an app that drops two strangers into an empty message thread has reproduced exactly that difficulty on a smaller screen.",
     "And the whole thing only works in the moment. A person is in that bar for two hours. Anything that takes a profile, a questionnaire and a matching algorithm has missed the evening it was supposed to be part of."],
    ("Opportunity", "Put a place between the two people",
     "A venue is public, chosen, temporary and shared. It solves the privacy problem and supplies the first thing to talk about at the same time.")),

  discovery=None,
  insight=dict(
    quote="Nobody wants to announce where they are. Plenty of people are happy to announce which bar they are in.",
    body=["Those sound like the same statement and are not. A live location is continuous, precise and involuntary-feeling; a check-in is a single, deliberate act attached to a public place you already walked into.",
          "Building the product around the venue rather than the person changed what the interface had to show. There is no map of people anywhere in it \u2014 only a list of places, and inside a place, a list of the people who chose to say they were there."]),

  solution=dict(
    lead="Places first, people second, and nothing visible until someone opts in.",
    body=["Three tabs carry the entire product: Feed is the list of venues near you, Chat is the conversations that came out of them, and Profile is four facts about you. Nothing else was added, because the app is used standing up, in a loud room, for a couple of hours.",
          "Everything below that is one level deep. There is no discovery layer, no feed of people and no map \u2014 the venue does that work, and the rest of the app exists to get you into one and then out of the way."],
    decisions=[
      ("The list is of places, not people",
       "Photograph, name, address, distance, guest count \u2014 and \u2018You are here\u2019 on the one you checked into.",
       ["Leading with venues means the app never has to show a person on a map. The nearest thing to a location it reveals is one a user typed themselves by choosing to check in, and that state is marked plainly on the card as <em>You are here</em>.",
        "Each venue carries how many people are currently checked in and how far away it is, to two decimals. Both are decision information rather than decoration: thirty-two guests and 0.05 km is a different evening from four guests and 1.68 km, and nothing else on the card distinguishes them."]),
      ("Guests are behind the check-in",
       "Feed and Guests as two tabs inside a venue, with a photo carousel above them.",
       ["Reciprocity is the rule that makes this safe to use: you can see who is here because you have said you are here too. It removes the lurker, and it removes the need to explain a privacy model in a paragraph.",
        "A guest row is a photo, a first name, an age and a gender mark \u2014 nothing else, and no message button on the row. Anything richer turns a bar into a dating profile, which is a different product with a different tone. The venue keeps its own like count, so popularity attaches to the place rather than the people in it."]),
      ("Chat is ordinary on purpose",
       "A search box, unread counts and timestamps. Nothing invented.",
       ["The conversation is the payoff, not the place to be clever. Anything unfamiliar here \u2014 disappearing messages, gimmicked composers, a novel list \u2014 would make people hesitate at exactly the moment the product is supposed to be working.",
        "So it looks like every messaging app anyone already uses, which is the highest compliment a chat screen can be paid. The only thing worth designing is how you got into the thread, and that happened two screens earlier."]),
      ("A profile with four fields",
       "Photo, name, gender, age \u2014 and a mute switch.",
       ["No bio, no interests, no prompts. Every field a profile gains is a field somebody is judged on before they have spoken, and the venue was supposed to do that work instead.",
        "Mute notifications sits on the profile rather than in a settings tree, because a social app that pings you in a bar you are already sitting in is a social app you delete."]),
      ("A mark that means two people",
       "Two interlocking rings, and a welcome screen that says nothing else.",
       ["The identity had to work at the size of an app icon and stay legible on a photograph of a dim room, so it is one shape with no wordmark inside it. Two rings overlapping, each with an eye, is the shortest possible statement of what the app is for.",
        "The opening screen carries only that mark. A product about meeting people in the next twenty minutes should not begin with a value proposition."]),
    ]),

  outcome=dict(
    lead="A social app that never shows you a person on a map.",
    body=["The venue model resolved the two hardest problems at once: it gave the product a privacy rule a user can hold in their head, and it gave every conversation a subject before the first message.",
          "It also kept the interface to three tabs and a profile with four fields, which is the right size for something opened between two drinks rather than studied at home."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["The instinct with a proximity product is to make proximity the feature. Making it a consequence instead \u2014 of choosing a place \u2014 is what made it usable by people who would never switch on a live location.",
          "If I revisited it, the check-in would need an expiry that is visible in the interface. A guest list that quietly includes people who left an hour ago is the failure mode that would erode trust fastest, and thirty-two guests is only reassuring if the number is true."]),
),

"opla-delivery": dict(
  headline="Three tabs shaped like a working day: Opla Delivery",
  sub="The courier app \u2014 what to collect, what to deliver, what you already did \u2014 with a leaderboard and the day\u2019s earnings behind the same screen.",
  role="UX/UI Designer", timeline="2021", team="Client product, engineering",

  challenge=C(
    "The courier is the only person in the delivery chain who is standing up.",
    ["Everybody else in the system \u2014 dispatcher, warehouse, support \u2014 is at a desk with two hands free. The courier is outdoors between two drops, holding a parcel, glancing at a phone for a few seconds at a time.",
     "There is no session in the usual sense. There are twenty ten-second sessions across a shift, each with exactly one thing to do, and the interface has to be re-enterable at any point without losing where you were.",
     "The information itself is also more awkward than it looks. A Georgian address is rarely enough to find a door \u2014 the useful part is \u2018intercom 36B, left door from the lift\u2019, which no address field has a place for.",
     "And the app holds something personal: how the courier is ranked against their colleagues, and how much they have earned today. Putting pay inside a work tool changes how often it is opened and how much it is trusted."],
    ("Constraint", "Every interaction happens between two stops",
     "One screen, one glance, one action \u2014 and the ability to pick up exactly where the last glance ended.")),

  discovery=None,
  insight=dict(
    quote="A courier does not have orders. They have a pile to pick up and a pile to drop off, and the day ends when both are empty.",
    body=["That sentence became the navigation. Three tabs \u2014 to collect, to deliver, history \u2014 rather than the usual orders / map / profile, because those are the two piles and the record of the ones already cleared.",
          "It also fixed the density question. Somebody working through a pile wants to see the pile, so the list is a table rather than a stack of cards: twenty jobs on one screen instead of four."]),

  solution=dict(
    lead="A table you can scan, a row that opens where it sits, and one orange action per screen.",
    body=["Each tab is a dated table with three columns \u2014 order number, address, time \u2014 grouped under day headings with alternating row shading, so a shift reads as a list rather than a feed. Tapping a row expands it in place.",
          "The delivery tab can flip between the list and a map with numbered pins showing the sequence. Ratings and earnings sit behind the same shell as a three-section accordion."],
    decisions=[
      ("The list is a table, not a stack of cards",
       "Order number, address, time \u2014 under a date heading.",
       ["Cards are the default for mobile lists and they are wrong here. A courier is working through a pile and needs to see the size of it; a card layout would show four jobs where a table shows twenty.",
        "Three columns is the whole record at a glance. Alternating row shading does the separating rather than borders or gaps, which keeps the density readable without costing vertical space."]),
      ("A row opens where it sits",
       "Full address, a map link, the call time, and the action \u2014 inline.",
       ["Navigating to a detail screen and back loses the courier\u2019s place in a list of twenty. Expanding in place means the surrounding rows stay put, which matters far more when the screen is being read in three-second bursts.",
        "The expanded row carries only what is needed to act: where it is, when it was called in, a link to the map, and the button. Everything else waits for the detail view."]),
      ("Two tabs, because it is two piles",
       "To collect, and to deliver.",
       ["A single \u2018orders\u2019 list mixes two different physical states \u2014 a parcel that is still at a shop and a parcel already in the bag. Splitting them means each tab empties over the course of the shift, and an empty tab is the clearest possible progress indicator.",
        "The delivery rows carry a van mark and an assignment time that the collection rows do not, because those are the two facts that only matter once something is in your hands."]),
      ("The map is a view, not a tab",
       "A list/map toggle on the same set, with numbered pins.",
       ["Making the map its own tab would split one job across two places. Toggling keeps it as a second reading of the same orders \u2014 and the pins are numbered rather than identical, so the map answers <em>what order do I do these in</em> rather than just <em>where are they</em>.",
        "Under the map sits the current order with a comment field carrying what an address cannot: <em>intercom 36B, left door from the lift</em>. That line is the single most valuable field in courier software and it is given its own label rather than being appended to the address."]),
      ("You cannot mark it delivered from the sofa",
       "\u201812 minutes until arrival\u2019, and the button greyed out until then.",
       ["Proof of delivery is worth nothing if it can be tapped early. The button is disabled with the reason written directly underneath it, so a courier who reaches for it sees why rather than assuming the app is broken.",
        "The detail screen puts the recipient\u2019s name, the full address and a phone number with its own call button in reach. Calling ahead is the most common recovery action in delivery, and it should never be more than one tap from the address that failed."]),
      ("Two named outcomes, not a swipe",
       "\u2018Yes, delivered\u2019 or \u2018No, return it\u2019.",
       ["Handing over a parcel is a financial and legal event, so it gets a modal that restates the order number, the recipient and the address before anything is confirmed. A swipe or a checkmark is too easy to do by accident with a parcel in the other hand.",
        "The failure path is offered in the same breath and written as a sentence rather than as <em>Cancel</em>. A courier who cannot complete a drop needs a route through the app, not a dead end that leaves the job open."]),
      ("History is searched by date, because that is how disputes arrive",
       "A date range, a search field, and the same table.",
       ["\u2018Where was my parcel on the twelfth\u2019 is the question this tab exists to answer, so the calendar is at the top rather than in a filter sheet. The range shows as plain text \u2014 01.12.20\u201318.12.20 \u2014 and stays visible.",
        "The rows are the identical component from the other two tabs. Once a courier has learned the table, they have learned the whole product."]),
      ("The leaderboard has real names on it",
       "A ranked bar chart of couriers, with your own position stated.",
       ["This is the decision in the project that I would still argue about. A named ranking is genuinely motivating near the top and quietly punishing near the bottom, and it is the client\u2019s call rather than the designer\u2019s.",
        "What design could do was give the courier their own numbers alongside it \u2014 current position, deliveries completed, average delivery time, percentage of target \u2014 so the chart is context for a personal figure rather than the only thing being shown."]),
      ("Pay sits in the same accordion as performance",
       "Today, this week, this month \u2014 under a rising line.",
       ["Earnings are the reason this section gets opened, and separating them from the ranking would have implied the two are unrelated when the whole point of the ranking is that they are.",
        "Three totals and one line is deliberately all of it. A courier checking pay between drops wants a number, not a breakdown \u2014 and a rising line is legible in the second and a half this screen actually gets."]),
      ("A login with nothing on it",
       "A wordmark, two fields, one button.",
       ["No marketing, no social sign-in, no \u2018create an account\u2019 \u2014 couriers are issued credentials, so every one of those would be a dead end dressed as an option.",
        "The single instruction above the fields says what to enter. On a tool people use at six in the morning, the correct amount of onboarding is one sentence."]),
    ]),

  outcome=dict(
    lead="A work tool that empties as the day goes.",
    body=["Two piles that shrink, a history that answers the questions support actually asks, and a ratings section where the courier\u2019s ranking and pay sit in the same place.",
          "One table component carries every list in the product, so the whole app is learned once and the build stays small."]),

  reflection=dict(
    title="What I would keep, and what I would push back on",
    body=["Shaping the navigation around the physical state of the parcels rather than around a database entity is the decision I would repeat. \u2018To collect\u2019 and \u2018to deliver\u2019 are the same records with a different status flag, and treating them as one list would have been technically tidier and much worse to work with.",
          "The named leaderboard is the part I would question harder now. It is effective and it is not neutral \u2014 being visibly last among your colleagues every day is a real cost to somebody, and if I revisited it I would want the ranking anonymised below the top few, with the personal figures kept exactly as they are."]),
),

"opla-fulfilment": dict(
  headline="A picking list that counts down: Opla Fulfilment",
  sub="The in-store picker\u2019s app \u2014 scan-verified grocery picking, and a receipt honest enough to name what could not be supplied.",
  role="UX/UI Designer", timeline="2021", team="Client product, engineering",

  challenge=C(
    "Picking groceries for somebody else is a job where being fast and being right pull in opposite directions.",
    ["An order arrives as a list of quantities \u2014 seventeen of one bread, two kilos of apples \u2014 and a picker walks a shop floor assembling it against a clock. Every second spent checking is a second lost, and every check skipped is a wrong item in somebody\u2019s bag.",
     "Groceries make the verification harder than parcels. Four breads from the same bakery differ by a word on the label, and the picker is holding a basket while reading a phone.",
     "Shortages are constant and unavoidable. Half the orders cannot be filled completely, so \u2018what happens when the shelf is empty\u2019 is not an edge case \u2014 it is a core flow, and it ends in somebody\u2019s money.",
     "And it is the same company as the courier app, so the two tools had to feel like one system operated by two different jobs."],
    ("Constraint", "One hand, a basket in the other, and a clock running",
     "Every screen has to be readable at arm\u2019s length and actionable with a thumb.")),

  discovery=None,
  insight=dict(
    quote="A picker does not want to know what is in the order. They want to know how much of it is left.",
    body=["A list of everything you must collect is demoralising at the start and useless in the middle. The same list phrased as a remainder tells you where you are in the job every time you look at it.",
          "So the counting runs everywhere: how many kinds of product an order contains before it is opened, how many units of the current line are still needed, and how many lines are left on the button that finishes the job."]),

  solution=dict(
    lead="A worksheet that shrinks, a scan that verifies rather than enters, and a receipt that admits what is missing.",
    body=["Three tabs carry the shift \u2014 new orders, ready to send, history \u2014 in the same table component as the courier app, so the two roles share one product. Opening an order gives a line-by-line worksheet where each row states what to find, how many, and how many remain.",
          "Picking a line opens a full-screen scan with the required quantity already on it. Everything that can go wrong \u2014 the wrong code, an unreadable label, an empty shelf \u2014 has a named state rather than an error toast."],
    decisions=[
      ("Count kinds, not items",
       "The order list shows \u201827 kinds\u2019 rather than a total quantity.",
       ["The number that predicts how long a pick takes is how many different products it contains, not how many units. Seventeen of one bread is one stop; seventeen different things is seventeen.",
        "It is the only figure on the row besides the number and the time, because a picker choosing what to start is making exactly one judgement: how big is this."]),
      ("The page counts down, not up",
       "\u201812 left to prepare\u2019 on the line, \u201813 positions remaining\u2019 on the button.",
       ["Progress bars are for people watching; remainders are for people working. Every number on this screen is phrased as what is still owed, so a glance answers \u2018am I nearly done\u2019 without any arithmetic.",
        "A finished line greys out and takes a tick rather than disappearing. The list stays the same length all the way through, which is what lets a picker keep their place in it while walking."]),
      ("The quantity is on screen before the scan",
       "The product card sits above the scan target, with the number in orange.",
       ["Scanning is verification, not data entry \u2014 the picker already knows what they are looking for. Putting the photograph, the name, the barcode and the required count above the camera means the scan confirms a decision rather than announcing one.",
        "The count repeats under the frame as the remainder, so the same number is visible whether the picker is looking at the top or the bottom of the screen."]),
      ("A scan is confirmed, not assumed",
       "\u2018This product is ordered \u2014 17 units\u2019, then Add, with Cancel underneath.",
       ["A barcode reader that commits on read will eventually add something twice, and in a shop that means a wrong basket and a refund. One tap between the read and the record costs a second and removes an entire class of error.",
        "Cancel is offered in the same panel and written plainly, because the most common reason to abandon a scan is realising you picked up the wrong size."]),
      ("The wrong product gets its own screen",
       "Red on dark: \u2018the product with this code is not in this order\u2019.",
       ["This is the error the whole app exists to prevent, so it is not a toast that slides away while the picker is looking at a shelf. It takes the screen, states the problem in one sentence and offers two exits: try again, or back to the list.",
        "Inverting to dark with a red mark makes it unmistakable at arm\u2019s length in a bright shop \u2014 the only red in the entire product, spent on the only thing that must never be missed."]),
      ("Typing the barcode is a first-class route",
       "\u2018Or find by barcode\u2019, with a filtered list underneath.",
       ["Labels get torn, frozen, wet and creased, and a scanner that fails on the seventh item stops the shift. Manual entry sits one tap from the scanner rather than three levels down in a settings menu.",
        "It filters the order\u2019s own products as you type rather than searching the whole catalogue, so the shortcut cannot become a way to add something that was never ordered."]),
      ("Two timestamps are the whole service level",
       "Ordered at, prepared at \u2014 as two columns.",
       ["The ready-to-send tab exists so somebody can see how long orders are sitting. Putting the two times side by side makes the gap between them readable without a calculation, which is the only number a shift supervisor actually wants.",
        "It is the same table as every other list in both apps. One component, learned once, used by two jobs."]),
      ("The row opens to what was actually picked",
       "Line items with photographs, inside the row.",
       ["A packed order is checked far more often than it is read, so expanding shows the assembled contents rather than a summary. Photographs make that check possible at a glance instead of by reading barcodes.",
        "It expands in place for the same reason as the courier app \u2014 a supervisor working down a list should not lose their position to look at one order."]),
      ("The receipt says what it could not supply",
       "Totals, then the shortfall, then the refund amount.",
       ["This is the decision I am proudest of in the project. A grocery order that arrives short is the moment a customer decides whether to order again, and most systems handle it by quietly charging less and hoping nobody notices.",
        "Here the receipt lists the missing items by name and quantity and states the amount going back to the account. Naming a failure and pricing it is more reassuring than a total that silently does not match \u2014 and it turns the delivery driver from somebody with bad news into somebody handing over a document that already explains itself."]),
      ("A login with nothing on it",
       "A wordmark, two fields, one button.",
       ["Staff are issued credentials, so social sign-in and \u2018create an account\u2019 would be dead ends dressed as options. One sentence of instruction is the right amount of onboarding for a tool used at six in the morning.",
        "It is identical to the courier app\u2019s login. Two different jobs, one company, and the first screen of both says so."]),
    ]),

  outcome=dict(
    lead="A worksheet that empties, and an order that is honest about itself.",
    body=["Pickers work down a counting-down list with scan verification at every line and a named state for each way it can fail; supervisors read two timestamps to see what is sitting.",
          "The receipt closes the loop by naming shortfalls and refunds rather than hiding them, and the whole product shares its shell, table and login with the courier app \u2014 one system, two jobs."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Phrasing every number as a remainder rather than a total is a small change with a disproportionate effect on a repetitive task. It is the difference between a list you are facing and a list you are finishing.",
          "Designing the shortfall properly is the other. Teams spend their effort on the path where everything is available, and then the flow that decides whether somebody orders again gets built in an afternoon. On a grocery product it deserves the opposite ratio."]),
),

"tichera": dict(
  headline="A marketplace that borrowed its own plumbing: Tichera",
  sub="A two-sided tutoring platform \u2014 the public marketplace, the student and tutor dashboards, the calendar and the classroom \u2014 built by connecting the tools tutors already used rather than rebuilding them.",
  role="Product Designer", timeline="2021 \u2014 2022", team="Founders, engineering",

  challenge=C(
    "A tutoring marketplace is three products pretending to be one, and it only pays for itself if somebody books twice.",
    ["There is a directory, where a student finds somebody who teaches chemistry at a price they can afford. There is a scheduling system, which has to reconcile two calendars across time zones. And there is a payments system, which has to hold money, release it, and handle the argument when a lesson does not happen.",
     "Only the first of those is a design problem. The other two are years of engineering, a payments licence in every market, and a support team \u2014 for a product with no users yet.",
     "And the marketplace is only half the product. The moment somebody pays, they land in a signed-in workspace that has to carry the rest of the relationship: when is my class, how do I join it, what did the tutor send me, this session did not happen. Most marketplaces design that half last, if at all \u2014 which is exactly the half that decides whether there is a second booking."],
    ("Opportunity", "Own the choosing and the teaching, borrow the rest",
     "The two things only this platform can do are helping a student pick the right person, and holding the relationship afterwards. Scheduling, payment and video can be somebody else's problem for as long as the interface is honest about it.")),

  discovery=None,
  insight=dict(
    quote="Tutors did not need us to build a calendar. They needed us to be the reason someone opened it.",
    body=["Every tutor already had a Calendly link, a PayPal.me link and a Google account, and all three worked perfectly well. Rebuilding any of them would have taken months and produced something worse.",
          "So the platform is deliberately thin where it can be and thick where it cannot. The booking hands off to the tutor's own calendar and payment link; the classroom embeds Meet. What is built from scratch is the part nobody else was doing \u2014 the directory, the reputation layer, and a workspace that opens on what is happening next."]),

  solution=dict(
    lead="One product in two halves: a directory that earns a booking, and a workspace that survives it.",
    body=["Signed out, Tichera is a marketplace. You browse tutors by category, compare on four facts, read reviews and reserve a session on a profile that carries everything a decision needs.",
          "Signed in, it becomes a workspace down a slim icon rail \u2014 home, calendar, classroom, notifications, settings. The same shell serves both sides of the market: the tutor creates courses and events, the student joins them, and neither has to learn a different product. Choosing Learn or Teach at sign-up changes what you see, not who you are."],
    decisions=[
      ("The profile is where the money decision happens",
       "Photo, subject, rating, hourly price, About Me and reviews \u2014 on one screen.",
       ["Every other surface in the marketplace exists to deliver somebody here. So the profile has to answer the whole question in one scroll: who is this person, are they any good, what do they cost, and can I book them now.",
        "Price sits in the right-hand rail directly above Reserve, with the Calendly and PayPal steps visible beneath it before the button is ever pressed. Nobody discovers how the booking works after committing to it."]),
      ("Reserve is two steps, and neither belongs to us",
       "Step 1 the tutor's Calendly. Step 2 the tutor's PayPal.",
       ["The modal is honest about what it is: a numbered handoff to two external tools, in the order they have to happen. Disguising that as a native checkout would have implied a guarantee the platform could not make.",
        "It also made tutor onboarding almost free. A tutor pastes two links they already own into their settings, sets an hourly price, and is bookable \u2014 no bank details, no verification queue, no waiting for the platform to approve them."]),
      ("One account, two directions",
       "Learn or Teach at sign-up, and a switch you can change later.",
       ["Splitting a marketplace into two account types is the standard move and it is usually wrong \u2014 it forces a decision at the least informed moment and traps people who are both. The same person can tutor chemistry on Tuesday and take a Spanish lesson on Thursday.",
        "The How it works page follows the same rule. One page, a Teacher / Student toggle, and the same steps told from each side, so the two halves of the market can read each other's version and know what to expect."]),
      ("The tutor card is four facts",
       "Photo, name, subject, rating, hourly price \u2014 then filter and sort.",
       ["In a grid of a hundred tutors the card has one job: support a comparison. Anything richer slows the scan, and anything less makes the price the only variable, which is a race the good tutors lose.",
        "Filtering by price and sorting explicitly are the two controls a student actually reaches for. The category tree does the rest of the narrowing before the grid is ever seen."]),
      ("The dashboard opens on time, not on identity",
       "Upcoming events beside notifications, archive below.",
       ["Nobody opens this to manage an account. They open it because a class starts in ten minutes \u2014 so the home screen answers what is happening now, what is happening next and what did I miss, in that order.",
        "A class about to start announces itself as a toast with Join and Decline on it rather than waiting to be found. The most time-critical action in the product should not require navigating to it, because a missed lesson is a refund and a bad review."]),
      ("The week carries six states, colour-coded once",
       "Requested, confirmed, ongoing, pending, completed, cancelled.",
       ["A tutoring calendar is not full or empty \u2014 it is six degrees of committed, and the difference between requested and confirmed is the difference between hoping and being paid.",
        "The legend sits beside the grid permanently rather than in a tooltip, because a colour system with six values is not one anybody memorises in a week. Create course and Create event sit here too, where the thing being made will appear."]),
      ("Use Google Meet and say so",
       "The classroom embeds Meet rather than building a video product.",
       ["Building video for a tutoring marketplace is months of work to arrive somewhere worse than free. Embedding it kept a small team on the part that was actually theirs.",
        "It is presented plainly rather than skinned to look proprietary \u2014 a tutor who already knows Meet has nothing to learn, which is the entire benefit of borrowing it."]),
      ("Reporting a problem starts with the lesson",
       "The tutor, the subject and the exact session, above the form.",
       ["Without escrow the platform cannot arbitrate a payment, but it can make complaining easy and specific. A form that begins with a blank text box makes the user reconstruct which class they mean.",
        "Opening with the session already identified \u2014 name, subject, date and time \u2014 turns the report into one sentence of actual content, and three named categories mean most arrive already routed."]),
      ("Notifications sorted by what they ask of you",
       "Messages, updates and important, as filters over one list.",
       ["A message from a tutor needs a reply; a platform update needs nothing. Merged into one stream, the ones that matter get lost among the ones that do not.",
        "Read state is a checkbox rather than a subtle change of weight, because this list is triaged rather than read."]),
    ]),

  outcome=dict(
    lead="A marketplace that shipped without a payments licence, and a workspace that gave it a second booking.",
    body=["Tutors publish a profile, paste two links and set a price; students search, compare, read reviews and book. Afterwards both sides share one workspace \u2014 a six-state calendar, the classroom, notifications, settings and a route to report a session that failed.",
          "The platform never touches money and never holds a calendar, which is what let it exist at all. The design language \u2014 teal, coral, flat editorial illustration, generous white space \u2014 was built to make a directory of strangers feel like a school rather than a listings site."]),

  reflection=dict(
    title="What I would keep, and what the trade-off cost",
    body=["Borrowing scheduling, payment and video was the right call for launch and it has a real price: with no escrow, the platform cannot arbitrate a lesson that did not happen. Reviews are the only protection a student has, which puts far more weight on the rating system than it was designed to carry. If I revisited it, that is where the next version of the work would go.",
          "On a small team, deciding what not to build is most of the design work \u2014 and the honest version is admitting in the interface which parts are somebody else's. The other lesson is duller. Placeholder copy survived into flows people actually see, and on a marketplace, where the entire product is asking a stranger to trust another stranger, unfinished text is not a cosmetic bug."]),
),

"meetsland": dict(
  cover="card",
  headline="A dating product is a safety product with a nice interface: Meetsland",
  sub="An online dating platform \u2014 profiles, matching, chat and video \u2014 where the design work that mattered most was the part nobody screenshots.",
  role="Product Designer", timeline="2022", team="Founders, engineering",

  challenge=C(
    "Everything a dating site does well is invisible, and everything it does badly is a headline.",
    ["The visible half is easy to describe: profiles, browsing, matching, messaging, video calls, a premium tier. Every competitor has the same list, so none of it is a reason to choose one.",
     "The half that decides whether people stay is moderation, reporting, blocking and what happens after somebody behaves badly \u2014 and it is designed last, if at all.",
     "There is also an asymmetry nobody likes discussing: the same feature feels like discovery to one person and exposure to another, and the interface has to be built for the one with more to lose."],
    ("Opportunity", "Design the report before the match",
     "A platform is judged on its worst interaction. Building the safety surfaces first changes what the rest of the product is allowed to do.")),

  discovery=None,
  insight=dict(
    quote="The premium feature people actually want is control, not visibility.",
    body=["Paid tiers in this category usually sell reach \u2014 be seen by more people. The subscription here leads with the opposite: see who liked you, and decide who can see you.",
          "That reframes the upgrade from vanity to agency, and it aligns the business model with the safety model rather than against it."]),

  solution=dict(
    lead="Browse, match, talk \u2014 with the controls at every step rather than in a settings page.",
    body=["Profiles are built from a photo and a short set of facts, browsed by age, location and interests, with matches suggested from stated preferences and previous behaviour. Conversation moves from text to video inside the platform, so nobody has to hand over a phone number to find out whether there is anything there.",
          "Visibility, blocking and reporting sit alongside those actions rather than three levels down, and events and group activities give people a lower-stakes way to meet than a one-to-one first message."],
    decisions=[
      ("Video before phone numbers",
       "Calls happen inside the platform.",
       ["The riskiest step in online dating is the one where the conversation leaves the app, because everything protective is left behind with it. Keeping video in-platform means a person can find out whether somebody is real without giving away a way to be contacted forever.",
        "It also compresses the timeline honestly \u2014 a five-minute call answers more than a fortnight of messages, and both people know it."]),
      ("Controls next to the action",
       "Blocking, reporting and visibility where they are needed.",
       ["A safety control buried in settings is a safety control that gets used after the damage. Putting them on the profile and in the conversation means they are reachable at the moment somebody actually wants them.",
        "The moderation team behind them is stated in the product rather than implied, because knowing a human will read the report is most of what makes people file one."]),
      ("Premium sells agency",
       "See who liked you; control who sees you.",
       ["Selling reach makes the platform louder for everyone and worse for the people already receiving too much attention. Selling control does the opposite, and it is the thing users ask for first.",
        "Group events and activities sit outside the paywall on purpose \u2014 the lowest-pressure way to meet somebody should not be the one behind a subscription."]),
    ]),

  outcome=dict(
    lead="The unglamorous half, designed on purpose.",
    body=["Meetsland ships the expected set \u2014 profiles, matching, chat, video, premium \u2014 with the safety surfaces designed alongside them rather than retrofitted after the first incident.",
          "The premium proposition doubles as the safety proposition, which is the rare case where the commercial and the ethical argument point the same way."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Designing the report flow before the match flow changes what you are willing to build. Several features that look good in a pitch quietly disappear once you have written what happens when they are misused.",
          "I would also push harder on the empty state. Every dating product launches with too few people on it, and pretending otherwise is how the first thousand users leave."]),
),

# ── brand & web, shorter but same shape ───────────────────────────────
"mvb-redesign": dict(
  headline="Selling two people, not a programme: MVB Club",
  sub="A redesign for a London online-coaching business \u2014 one scrolling page and a members\u2019 login, built to turn a stranger into an application.",
  role="UX/UI Designer", timeline="2020 \u2014 2021", team="Client, engineering",

  challenge=C(
    "The product is two coaches, and the competition costs nine pounds a month.",
    ["MVB Club is George and Miles \u2014 thirteen years between them \u2014 selling personal online coaching: a workout and meal plan written for you, direct contact with the coaches, a training app and a video library.",
     "Everything in that list except the last two words is also offered by a fitness app for a fraction of the price. The service is expensive, recurring, and asks a stranger to hand over their body composition and their diet to somebody they have never met.",
     "So the site is not selling features. It is selling the belief that a specific person will read what you send them and write back \u2014 which is the one thing an app cannot do, and the hardest thing to make credible on a landing page.",
     "It also had to be one page. This is a two-person business; a site with twelve routes through it is a site nobody maintains."],
    ("Opportunity", "Put the coaches in front of the offer",
     "If the visitor meets George and Miles before they meet the price list, every claim afterwards has somebody attached to it.")),

  discovery=None,
  insight=dict(
    quote="An app can write you a programme. It cannot be somebody who knows your name.",
    body=["That is the entire commercial argument, and it decided the order of the page. The coaches are named and photographed in the second section, before anything is offered, and the promise underneath the offer is written in the first person plural: <em>we personally coach you all the way</em>.",
          "It is repeated verbatim at the bottom of the page. On a single-scroll site the same sentence in two places is not redundancy \u2014 it is the argument bracketing everything in between."]),

  solution=dict(
    lead="One scroll: welcome, the coaches, what you get, proof, what is included, apply.",
    body=["Each section is announced by its own name set huge and hollow behind the real heading \u2014 ABOUT, STORIES, PLANS, CONTACT \u2014 so a page with no navigation still has landmarks you can scroll to and recognise.",
          "The sections are separated by a diagonal notch rather than a straight edge, and threaded together by a thin orange rule that runs down the centre between them. Photography is the client\u2019s own, desaturated, with orange and white doing all the signalling."],
    decisions=[
      ("A welcome, not a pitch",
       "\u2018Welcome to MVB\u2019 over a photograph, and nothing else.",
       ["The hero makes no claim and lists no benefit. On a service sold on relationship, the first screen is an introduction \u2014 the argument starts one scroll later, once there are faces attached to it.",
        "The band ends in a diagonal notch rather than a horizontal edge. It is the page\u2019s one structural mannerism, repeated at every section boundary, and it does the job a grid usually does on a site with no columns to speak of."]),
      ("Name the two people and count the years",
       "\u2018George & Miles\u2019, a photograph of them, thirteen years.",
       ["A number is what turns a claim into a fact. \u2018Thirteen years in the industry\u2019 is the most persuasive sentence on the page and it sits in the second section rather than in a footer.",
        "The photograph is them, not a stock athlete. Everywhere else on the site the imagery is anonymous training footage; here it is deliberately the two people you would be paying, looking at the camera."]),
      ("Four pillars, and the promise underneath the heading",
       "Programming, tracking, meal plans, coaching \u2014 numbered 01 to 04.",
       ["The offer is four things, so it is shown as four columns with hollow numerals and a line icon each, over a full-bleed training photograph turned down to grey. Rendering it as a list would have made a coaching service look like a pricing table.",
        "\u2018We personally coach you all the way\u2019 sits directly under the section title in orange, so the differentiator is read before the features rather than after them. The same four pillars reappear on the quiz result screen, with the same icons \u2014 one offer, told identically wherever somebody meets it."]),
      ("One long testimonial, not a wall of stars",
       "A single client, in his own words, with arrows to the next.",
       ["Richard\u2019s quote is four lines long and mentions injury setbacks and ups and downs. A curated five-star wall reads as marketing; a testimonial that admits the process was hard reads as a person.",
        "It occupies its own section with nothing competing for attention, because on a high-trust purchase the proof is not a supporting element \u2014 it is a step in the argument."]),
      ("The ask is an application, and it costs nothing",
       "A ticked list of what is included, APPLY NOW, and \u2018applying is non-committal\u2019.",
       ["The four inclusions are set as literal ticked rows on a dark card so the offer can be read in five seconds without a price anywhere near it. Naming a figure at this point invites a comparison with a nine-pound app, and that is the wrong conversation.",
        "The line under the button is the most important copy in the section. On a service this expensive the barrier is not doubt about quality, it is fear of being sold to \u2014 and \u2018applying is non-committal\u2019 removes that for the cost of three words."]),
      ("Close by repeating the promise and changing the verb",
       "The same headline again, and \u2018Get started\u2019 instead of \u2018Apply now\u2019.",
       ["Somebody who has scrolled the whole page has read the argument and is ready for a different word. \u2018Get started\u2019 addresses a decision already made; \u2018Apply now\u2019 addresses one still being considered.",
        "Repeating the headline verbatim closes the bracket opened four sections earlier. The visitor leaves having been told the same thing twice, which on a page with no navigation is how a message survives the scroll."]),
      ("The members\u2019 area wears the same clothes",
       "The marketing header and footer, around a four-element login.",
       ["Clients arrive at the login from an advert, an email or the site itself, and it is the first thing they see after paying. Handing it to a default framework would have made the product feel like a different company from the one that sold it.",
        "The form itself is deliberately plain \u2014 two fields, one orange button, a way back in if the password is gone, and the data policy in reach. There is nothing to design here except restraint."]),
    ]),

  outcome=dict(
    lead="A one-page argument that ends in an application.",
    body=["The site introduces the coaches, states the four things a client receives, proves it with one long testimonial and asks for an application that costs nothing to send \u2014 in a single scroll a two-person business can maintain.",
          "The visual system \u2014 orange on near-black, hollow landmark type, diagonal section cuts and the client\u2019s own photography \u2014 carries from the marketing page through the onboarding quiz to the members\u2019 login without a seam."]),

  reflection=dict(
    title="What I would keep, and what the device cost",
    body=["Leading with the people rather than the offer is the decision I would repeat on anything sold by a small team. The features are matched by every competitor; the names are not.",
          "The hollow section labels are the part I would handle differently. Setting a word at two hundred pixels behind every heading is a strong device and a completely unforgiving one \u2014 a typo that would pass unnoticed in body copy becomes the largest object on the screen. If the type is going to be that big, the words have to be locked before the layout is."]),
),

"mvb-quiz": dict(
  cover="card",
  headline="Four questions and an honest gate: MVB Club Quiz",
  sub="An onboarding quiz for a fitness coaching service \u2014 designed as a campaign rather than a form, and open about the fact that it ends in an email field.",
  role="UX/UI Designer", timeline="2021", team="Client, instructors, engineering",

  challenge=C(
    "Two people need this to do opposite things, and one of them wants it to be over.",
    ["The instructor needs enough about a person\u2019s life to write a real plan rather than a template with a name on it: what they are training for, what they have access to, who they are.",
     "The person answering arrived to get in shape, not to fill in a form. Every additional question is a chance to close the tab, and this one is reached from an advert rather than from an account they have already invested in.",
     "It is also, plainly, a lead capture. The business needs a name and an email at the end of it. Most quizzes of this kind hide that until the last screen and then spring it after the work has been done, which is exactly the moment it feels like a trick."],
    ("Opportunity", "Do the consultation first, ask last, and say what the email buys",
     "If the quiz genuinely narrows down a plan before it asks for anything, the email field at the end reads as the next step rather than as the toll.")),

  discovery=None,
  insight=dict(
    quote="Four questions is not a shortened questionnaire. It is the whole design decision.",
    body=["Gender, age, primary goal, training environment. That is the minimum an instructor needs to start writing, and everything beyond it was cut because it can be asked later by a human who is already in the conversation.",
          "Once the count was fixed at four, the rest of the work stopped being about pacing a long form and became about making four screens feel like something worth doing \u2014 which is a photography and copy problem more than a layout one."]),

  solution=dict(
    lead="A quiz that looks like the brand\u2019s advertising, not like its database.",
    body=["Every question is a full-bleed photograph of somebody training, with the answers as translucent bars stacked over the left third. The counter sits top-left in large type, the brand mark top-right, and a footer bar restates the instruction on every screen.",
          "The sequence runs intro, a held beat, four questions, then the result screen \u2014 where the plan is described, the name and email are asked for, and what happens next is stated in four words."],
    decisions=[
      ("Start is a slider, not a button",
       "\u2018Slide for start\u2019 on a track, over the trainers\u2019 own photograph.",
       ["A button is pressed by accident; a slider is a small deliberate act, and it sets the register for what follows \u2014 this is a thing you are doing rather than a page you are on.",
        "The trainers are named on the intro image. The quiz is answered more honestly when it is obvious that specific people will read it, so their faces appear before the first question rather than in an About section nobody reaches."]),
      ("A held beat before the first question",
       "A full-screen \u2018Get Ready\u2019 on black, then straight into 01.",
       ["Two words on an empty screen do more for pacing than any transition. It separates the marketing page from the questions, so the first question does not arrive while somebody is still reading a headline.",
        "It also borrows the language of the gym rather than the language of software, which is the register the whole product is trying to hold."]),
      ("One question per screen, on a photograph",
       "Answers as translucent bars over the left third.",
       ["A form shown all at once is judged before it is started. Dealt one at a time, each question is judged on its own \u2014 and at four questions the whole thing is over before anybody decides it is long.",
        "Putting the answers on a photograph rather than a white card keeps the quiz inside the brand\u2019s advertising rather than dropping into an anonymous form. The bars are translucent so the image survives underneath, which is what makes the screen look like a campaign frame."]),
      ("The counter is the largest thing on the page",
       "\u201801\u2019 large, \u2018/04\u2019 small beside it.",
       ["The denominator is the reassurance and it is visible from the first screen: this is four questions, and you are on the first. Making the number bigger than the question is the opposite of the usual hierarchy and it is deliberate.",
        "\u2018Go back\u2019 sits under it, quiet and always present. A quiz that cannot be corrected is a quiz people abandon rather than risk answering wrongly."]),
      ("Every question changes the plan",
       "Goal, and then the equipment you actually have.",
       ["The test applied to each question was what changes in the output if it is left blank. Fat loss and building strength are different programmes; a CrossFit box and \u2018travel a lot so always have limited equipment\u2019 are different programmes again.",
        "The answers are written as sentences people say about themselves rather than as categories. \u2018Build muscle and strength while leaning out\u2019 is how somebody describes their goal out loud, and recognising yourself in an option is what makes the answer accurate."]),
      ("The reassurance goes on the last question",
       "\u2018Your plan is already set, only one question left.\u2019",
       ["Drop-off clusters just before the end, when the effort is spent and the reward is still not visible. A line of copy at exactly that point is cheaper than any progress animation and does more.",
        "It is also true, which matters. By question four the instructor has enough to start, and saying so converts the last question from an obstacle into a formality."]),
      ("The gate is at the end, and it says what it is",
       "Name, email, and \u2018what you get\u2019 listed beside the field.",
       ["Asking for contact details after the work has been done is only fair if the person can see what they are exchanging them for. Programming, tracking, meal plans and online coaching sit next to the form as four plain icons, so the trade is legible at a glance.",
        "\u2018We can get back to you regarding your results\u2019 promises a person rather than an autoresponder, and a quiet \u2018Continues to web\u2019 gives anybody who does not want to hand over an address a way out that is not the browser back button."]),
    ]),

  outcome=dict(
    lead="Enough to write a plan, in four questions and a minute.",
    body=["Instructors receive the goal, the constraint and the basics they need to write something specific; the person answering gets a stated promise and a human follow-up rather than a confirmation email.",
          "Because the quiz is built from the brand\u2019s own photography rather than from form components, it can run as a landing page from an advert without looking like it belongs to a different product."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["The useful discipline on any onboarding questionnaire is to ask, for every question, what changes in the output if it is left blank. Four survived that test here, and the temptation to add a fifth came back on every review.",
          "The other one is about honesty in a funnel. A quiz that captures an email is not a problem; a quiz that pretends it is not capturing an email is. Putting the list of what you get next to the field it is asked for costs nothing and is the difference between a trade and a trap."]),
),

"marketcolor": dict(
  headline="An agency whose portfolio lives inside other people\u2019s channels: Marketcolor",
  sub="A London technical content agency working for finance, life sciences and technology \u2014 where the site had to prove thirteen years of craft without being able to show most of it.",
  role="UX/UI Designer", timeline="2020", team="In-house \u2014 London",
  live="https://www.marketcolor.co/",

  challenge=C(
    "The work is scripts, animation, reports and explainer video \u2014 and almost none of it is Marketcolor\u2019s to publish.",
    ["Marketcolor writes and produces for Nasdaq, Deutsche Bank, BNY, SWIFT, Google, IBM, the European Commission and around thirty other institutions. The output is scriptwriting, storyboard design, post-production, copywriting, print and digital reports, eLearning series.",
     "All of it ships under the client\u2019s name, inside the client\u2019s channels, often behind their login. An agency site in this position cannot run the usual case-study format \u2014 there is frequently no screenshot, no live link and no permission to describe the outcome in numbers.",
     "The audience does not help either. A marketing lead at a bank is not browsing for inspiration; they are checking whether this agency has done something serious for someone serious, in their sector, recently. Three questions, and a conventional portfolio grid answers none of them quickly.",
     "There was also a maintenance problem waiting. Agency sites decay because new work has to be designed in, so it stops being added \u2014 and a content agency with a stale site is arguing against itself."],
    ("Opportunity", "Publish the ledger, not the portfolio",
     "If every commission is one row \u2014 client, one sentence of scope, a date \u2014 then the site is a record rather than a showcase. It answers all three questions in a scan, and adding work becomes writing a line rather than designing a page.")),

  discovery=None,
  insight=dict(
    quote="The client\u2019s name is doing the persuading. Everything else on the row is just proving it happened.",
    body=["In this market, credibility transfers. \u2018Scriptwriting, design and post-production for the Nasdaq Eqlipse animated explainer\u2019 does more work than any amount of process narrative, because the reader already knows what Nasdaq\u2019s standard is.",
          "So the row was designed to carry exactly three things: who it was for, what was actually made, and when. No adjectives, no results claim, no case-study link \u2014 and consequently nothing that needs legal approval before it can be published."]),

  solution=dict(
    lead="One page, one reverse-chronological ledger, and a component that holds the standard as it grows.",
    body=["The site opens by stating what the agency is and where it operates \u2014 a technical content agency in London, working 09:00 GST to 16:00 EST, for finance, life sciences and technology. Two sentences that qualify the reader before they scroll.",
          "Below it the commission log runs continuously back to 2012. Long engagements carry a range rather than a point in time, and a commission that produced several pieces collapses into a numbered set inside its own row, so one relationship stays one entry instead of flooding the timeline.",
          "The showreel and the agency\u2019s own animated history sit at the top as the one place where the work can be shown rather than described, and contact is a phone number, an email address and a credentials deck \u2014 no form."],
    decisions=[
      ("A commission is one row, and the row is the component",
       "Client, one sentence of scope, a date. Nothing else.",
       ["Fixing the shape of the entry is what makes the page maintainable. Adding a piece of work is writing three fields, which anybody in the studio can do correctly, so the site keeps pace with the business instead of falling six months behind it.",
        "It is also the quality mechanism. The craft lives in the type, the rhythm and the spacing of a repeated element \u2014 so it is inherited by every future entry rather than negotiated per project. There is no layout for a non-designer to get wrong."]),
      ("Reverse chronology is the argument",
       "Newest commission first, running back to 2012.",
       ["For most content sites date order is a lazy default. Here it is the point: the visitor\u2019s real question is whether this agency is currently working, and at what level. The top of the page answers it before anything is read.",
        "The depth answers the second question by itself. A log that keeps going for thirteen years is a claim about longevity that no About page can make as convincingly."]),
      ("Multi-piece commissions collapse into one entry",
       "A numbered set inside the row rather than eight separate rows.",
       ["A single engagement that produced twenty-five videos would otherwise bury a year of other work. Nesting keeps the timeline readable and keeps the unit of the page a relationship rather than a file.",
        "The counter is shown plainly \u2014 a set of eight reads as a bigger engagement, which is information the visitor wants anyway."]),
      ("Qualify the reader in the first two sentences",
       "What we make, where we are, which sectors, which hours.",
       ["Naming the sectors filters honestly: the wrong client leaves quickly, which is the correct outcome for an agency this specialised. Stating the working window is a practical detail that matters enormously to a New York or Gulf client and appears on almost no agency site.",
        "It buys the ledger its context. Without those two lines a list of banks is just a list of banks."]),
      ("Contact is a phone number, not a funnel",
       "Call, email, or download the credentials deck.",
       ["A contact form implies a queue and a qualification process. At this end of the market the person getting in touch already has a budget and a deadline, and making them wait for a reply is a way to lose them.",
        "The credentials deck exists for the other route \u2014 the reader who has to circulate something internally before anyone picks up a phone."]),
    ]),

  outcome=dict(
    lead="A site that is a record of work rather than a presentation of it.",
    body=["The commission log carries hundreds of entries across roughly thirty named institutions and thirteen years, and it stays current because publishing new work costs a sentence.",
          "The standard holds structurally rather than editorially: whatever gets added inherits the same typography, spacing and rhythm, so the page cannot be eroded by the people who have to keep it alive."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["The constraint turned out to be the brief. Not being able to show the work forced a format that suits this audience far better than a case-study grid would have \u2014 a buyer at a bank wants evidence, not narrative, and evidence is a list.",
          "Marketcolor has been redesigned since I worked on it, and the ledger is still the spine of the site. That is the part I would defend anywhere: on any site somebody else has to maintain, put the quality in a repeated component and let the content be plain."]),
),

"miniso": dict(
  headline="Eleven hundred cheap things, and a basket worth designing: Miniso Georgia",
  sub="A redesign of the Miniso web platform \u2014 ten categories and ten thousand items, an average order too small to fuss over, and seventeen licensed collaborations that fit in none of the categories.",
  role="UX/UI Designer", timeline="2021", team="Client, engineering",

  challenge=C(
    "The catalogue is enormous, the items are cheap, and nobody arrives wanting a specific one.",
    ["Miniso carries over ten thousand product names across ten categories \u2014 household goods, travel and digital accessories, sport, personal care, toys, seasonal ranges and gifts. A listing page in a single section runs to eleven hundred results across thirty-eight pages. Nobody reads that, and nobody arrives knowing which of them they want.",
     "The economics make it harder. A basket of one twenty-lari item barely covers the delivery, so the site has to encourage several small additions \u2014 which is the opposite of the fast find-and-checkout flow most e-commerce is optimised for.",
     "The range is also far wider than the price suggests. A thirteen-lari soft toy and a certified digital accessory sit in the same shop, and one product template has to serve a keyring and something with a specification sheet.",
     "And a large share of the reason anybody visits is licensed: Disney, Barbie, Sanrio, Harry Potter, Toy Story, Minions, BT21, Coca-Cola and roughly ten more. Those are merchandising facts rather than categories, and no taxonomy will hold them."],
    ("Opportunity", "Design the basket as hard as the catalogue",
     "The first item is why somebody came. Everything after it is where the order value is made, so the cart deserves more design attention than it normally gets.")),

  discovery=None,
  insight=dict(
    quote="On a catalogue this size, the shop window matters more than the shelf.",
    body=["Eleven hundred results cannot be browsed, so the way in cannot be the grid. Category tiles, a recommendation band, discounts, new arrivals and the licensed collaboration are the actual navigation \u2014 curated entrances into a catalogue nobody could otherwise face.",
          "The corollary is that the cart is not the end of the journey. It is the last and best place to add a second item, which is why it carries a save-for-later shelf and a related-products carousel rather than just a total and a button."]),

  solution=dict(
    lead="Curated ways in, a filter rail that never moves, and a basket built for adding rather than finishing.",
    body=["The home page is a sequence of entrances: a promotional banner with four category tiles laid over it, then discounts, an editorial recommendation band, new arrivals, the licensed collaboration and best-sellers. Each is a route rather than an advert.",
          "Listing pages carry a left rail of collapsible category groups with checkboxes, a discount toggle and a price range, above a three-column grid with the result count stated. The product page changes depth by what is being sold, and the cart runs basket and order history as two tabs with a saved-items shelf underneath."],
    decisions=[
      ("Category tiles break the banner, on purpose",
       "Four shortcut cards laid over the promotional hero.",
       ["A promotional banner takes the best position on the page and is the least useful thing on it. Laying the category tiles across its lower half puts real navigation in the first screen without giving up the campaign slot.",
        "Each tile is a photograph of the product type on a flat colour ground \u2014 hand cream on pink, a backpack on blue, a plate on coral, a toy car on yellow. It reads as Miniso\u2019s own merchandising rather than as a menu."]),
      ("One editorial band, not a carousel of everything",
       "A large lifestyle photograph beside two stacked product cards, on near-black.",
       ["Between two rows of small product cards, a third row would have disappeared. Inverting to dark and giving one recommendation a full photograph makes the section read as a suggestion from the shop rather than as more inventory.",
        "The two cards stacked beside it carry the actual products, so the photograph can do mood while the offer stays specific. One button, no pagination \u2014 a recommendation that needs browsing is not a recommendation."]),
      ("Collaborations are a module, not a category",
       "A licensed band that repeats on the home page and on listing pages.",
       ["Miniso runs seventeen licensed partnerships at once, and each one cuts straight across the tree \u2014 Marvel is a cushion, a mug, a phone case and a bag simultaneously. A collaboration can never be a node in a taxonomy built from product types.",
        "So it is a recurring band instead, which can appear wherever traffic lands and be swapped for whichever partner is current. It gets editorial treatment \u2014 a full product photograph, a paragraph and one button \u2014 because at that moment the site is selling a collaboration rather than an item."]),
      ("A category page that opens with pictures",
       "Six banner tiles above the grid, and a discount badge that does not shout.",
       ["Landing in a section from search or a menu is the moment a shopper is least oriented. Six photographic tiles across the top say what is in here faster than a list of subcategory names, and they narrow the eleven hundred before a single filter is touched.",
        "Almost everything on this platform is discounted at some point, so the badge is a small red disc at the corner of the card rather than a banner across it. Same size, same position on every card \u2014 the eye learns it once and can then scan for it."]),
      ("Say how many results there are",
       "\u20181100 results\u2019 above the grid, and page 38 in the pagination.",
       ["Stating the size of the result set is what turns filtering from optional into obviously necessary. A shopper who sees eleven hundred understands immediately that the rail on the left is the tool, not decoration.",
        "The facet groups are collapsed by default with a chevron each, so the rail stays short enough to scan. On a general catalogue most shoppers do not know a category\u2019s vocabulary, and a wall of open facets teaches them nothing."]),
      ("One product template for a keyring or a phone",
       "Thumbnail rail, large image, and a right column that grows or shrinks.",
       ["The same page has to sell a thirteen-lari plush and a certified electronic accessory. The frame is fixed \u2014 gallery left, decision column right \u2014 and only the contents of that column change: colour swatches and capacity chips appear when they exist and are simply absent when they do not.",
        "Buy and save-for-later sit together under the price, one filled and one outlined. At this price point the hesitation is rarely about money, so the alternative to buying is not leaving, it is remembering."]),
      ("Specifications are a table, not prose",
       "Zebra-striped rows, label left, value right \u2014 under the description.",
       ["Anything with a spec sheet is compared across tabs, and comparison needs a fixed row order. Whatever has been filled in renders identically for every product that has one.",
        "The seller\u2019s own writing goes above it, in the description. Separating the two means loose marketing copy cannot contaminate the part being compared."]),
      ("Bundles are shown as an equation",
       "Product plus product equals a total, with buy and add-to-basket.",
       ["\u2018Also bought\u2019 usually means a carousel nobody reads. Rendering it literally \u2014 two items, a plus, an equals, one total \u2014 makes the offer legible in a second, which is all the attention it will get.",
        "Two commitments are offered because they are different intentions: buy this pair now, or add it and keep shopping. Collapsing them into one button loses whichever shopper it was not built for."]),
      ("The basket is a shelf, not a receipt",
       "Two tabs, a quantity stepper, and two actions on every row.",
       ["Basket and order history sit side by side, because \u2018where is my order\u2019 and \u2018what did I buy last time\u2019 are the same trip \u2014 and it keeps the account area almost empty, which for a shop selling twenty-lari items is the correct amount of account.",
        "Quantities are a stepper rather than a field, and the control fills in the moment it is pressed. On a page listing five near-identical rows, a shopper otherwise cannot tell whether the click landed on the one they meant."]),
      ("Saved items live under the basket",
       "A shelf with \u2018return to basket\u2019, and similar products below it.",
       ["Every row offers <em>save for later</em> beside <em>remove</em>. Deleting something you were unsure about is how an order shrinks; moving it down a shelf keeps it in the session, one link from coming back.",
        "The saved shelf sits directly beneath the basket rather than in an account page, with a related-products carousel under both. On a shop where the average item is twenty lari, this is the highest-intent surface in the product and the cheapest place to earn a second and third item."]),
    ]),

  outcome=dict(
    lead="A site that behaves like the shop it belongs to.",
    body=["Curated entrances replace an unbrowsable grid, the filter rail is stated and short, the collaboration appears wherever the traffic does, one product template covers a plush toy and a spec sheet, and the basket is built to grow rather than to close.",
          "Miniso had twenty-seven branches in Georgia by the time of this work, and the stores are cheerful and slightly silly \u2014 so the site ends in a yellow footer with the brand mascot sitting in the corner doing nothing functional at all. A grey utility footer would have closed every page in a different brand from the one the shopper had walked through."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Spending the design effort on the basket rather than the product page is the decision I would repeat on any low-value, high-volume catalogue. The product page settles a purchase somebody had already decided on; the basket is where the order actually gets bigger.",
          "Stating the result count is the smallest change with the largest effect. Eleven hundred is a number that makes a shopper reach for a filter, and hiding it just produces people scrolling page four of thirty-eight."]),
),

"home-market": dict(
  cover="card",
  headline="A shop for the kitchen counter: Home Market",
  sub="An Android tablet app for ordering food and household goods \u2014 designed for a device that lives in one room and gets used with wet hands.",
  role="UX/UI Designer", timeline="2021", team="Client, engineering",

  challenge=C(
    "A tablet is not a big phone, and a kitchen is not a sofa.",
    ["The device sits in one place, is used standing up, is shared by a household and gets touched with hands that have just been doing something else. That rules out the interaction patterns most shopping apps rely on.",
     "It is also the wrong shape for a phone layout stretched wide: a two-column grid at tablet size wastes the one advantage the device has, which is that the products can be shown large enough to actually see.",
     "The buying pattern is different too. Nobody browses groceries for pleasure \u2014 it is a recurring, forgettable task where the same forty items come round every week."],
    ("Opportunity", "Use the screen for the produce",
     "The single thing a tablet does better than a phone is show you what the food looks like. Everything else follows from that.")),

  discovery=None,
  insight=dict(
    quote="Nobody wants to shop for groceries. They want last week\u2019s order with three things changed.",
    body=["Treating a grocery app as a discovery experience misreads the task. The fastest possible route to a repeat order is the feature, and browsing is the exception.",
          "So reordering, wish lists and purchase history are primary rather than buried in an account section, and the beautiful large product imagery serves the items you have not bought before."]),

  solution=dict(
    lead="Reorder first, browse second, and everything big enough to tap without looking.",
    body=["Stores are filtered by category, price and location, with products shown large \u2014 the tablet\u2019s one real advantage. Previous purchases and saved lists sit at the top of the journey so a weekly shop is a review rather than a search.",
          "Payment details are saved for a one-touch checkout, orders are tracked in real time, and a barcode scanner ties the app to the fridge \u2014 scan an item to check its expiry or to put it straight back on the list."],
    decisions=[
      ("The repeat order is the front door",
       "History and saved lists ahead of the catalogue.",
       ["The weekly shop is ninety per cent identical to last week\u2019s. Making that the starting point turns a twenty-minute task into a two-minute one, which is the only reason somebody keeps using it.",
        "Discovery still exists \u2014 it is just not what greets somebody who came to reorder milk."]),
      ("Scan the fridge, not the catalogue",
       "Barcode scanning for expiry dates and instant re-adds.",
       ["Tying the app to the physical kitchen is what a stationary tablet can do that a phone in a pocket cannot. Scanning something you already own to check a date or reorder it closes the loop between the cupboard and the basket.",
        "It also gives the app a reason to be opened between shops, which is where most grocery apps lose the habit."]),
    ]),

  outcome=dict(
    lead="A shopping app that fits the room it lives in.",
    body=["Large product imagery, one-touch reordering, saved payment and real-time tracking, with a barcode scanner connecting the app to what is actually in the fridge.",
          "The layout uses the tablet's size for the products rather than for more columns of the same thing."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Designing for a device that never moves is a genuinely different brief. Reach, posture and who else in the house might pick it up all change what belongs on the screen.",
          "The habit question is the one I would keep asking: what makes somebody open this on a day they are not shopping?"]),
),

"asorti": dict(
  headline="Selling an occasion, not a product: Assorti",
  sub="Confectionery e-commerce, where the thing in the basket is usually for somebody else.",
  role="UX/UI Designer", timeline="2021", team="Product, marketing",
  live="https://www.assorti.ge/",

  challenge=C(
    "Nobody buys a cake the way they buy groceries.",
    ["A cake is bought a handful of times a year, almost always for an occasion, and almost always for someone else. There is no habit to lean on, no reorder pattern, no weekly rhythm — the shopper arrives with a date in mind and very little else.",
     "That makes the usual e-commerce moves work against you. Filters and specification tables answer questions a birthday shopper is not asking. What they need is to see it, believe it will look like the photo, and know it can be there on Saturday.",
     "The catalogue is also unusually wide for a bakery: whole cakes, single pastries, boxes, seasonal and fasting ranges, plus made-to-order designer cakes that are not really a product at all but a conversation."],
    ("Opportunity", "Photography is the product page",
     "For a cake, the image is not decoration around the description — it is the description. Everything else on the page exists to support a decision the picture has already started.")),

  discovery=None,
  insight=dict(
    quote="The catalogue is not a list of goods. It is a list of occasions.",
    body=["Reframing it that way settled a lot of arguments. Whole cakes, single pastries and boxes are not three product types competing for the same grid — they are three different moments: a celebration, a treat for yourself, something to bring to other people.",
          "Once the categories carried that meaning, browsing stopped needing filters. You pick the occasion and the range narrows itself."]),

  solution=dict(
    lead="A shop built to be looked at rather than searched.",
    body=["Product imagery runs full width and uncropped on a near-neutral ground, so the cake is the only saturated thing on screen. The rest of the interface is deliberately quiet.",
          "Price, discount and the add-to-basket control sit in a fixed relationship on every card, so the eye learns the pattern once and stops re-reading it."],
    decisions=[
      ("Occasions, not filters",
       "Categories that match how a purchase is actually decided.",
       ["Cakes, pastries, baked goods, sweet and fasting ranges — the split follows the reason for buying, not an internal product taxonomy. It removes most of the need for filtering on a catalogue this size."]),
      ("The photograph carries the page",
       "One consistent treatment, no crops, no busy backgrounds.",
       ["Every item is shot on the same neutral ground at the same angle, which does two things: it makes the range look like one brand, and it lets a shopper compare two cakes without the photography being a variable."]),
      ("Discounts that do not shout",
       "A small badge and a struck-through price, nothing more.",
       ["Confectionery discounting is frequent, so it had to be legible without turning the grid into a sale board. The badge sits at the card corner and the old price stays visible but recessive."]),
      ("Made-to-order treated as its own path",
       "Designer cakes lead to a conversation, not a basket.",
       ["A custom cake has no fixed price or lead time, so forcing it through the same checkout would fail. It gets its own route through the navigation and ends in a brief rather than an order."]),
    ]),

  outcome=dict(
    lead="A storefront that behaves like a shop window.",
    body=["Assorti runs at assorti.ge as the brand's online store, alongside the physical branches. Ordering, the confectionery school and events all live under one navigation.",
          "The visual system has held as the range has grown — new products drop into the same treatment without a design pass."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["I started this project with the wrong model in my head — an efficient basket, fast quantity controls, reorder. All correct for groceries and all wrong here. Someone buying a birthday cake is not optimising; they are trying to feel confident about a gift.",
          "The useful question was not 'how do we make this faster' but 'what would make you trust that it arrives looking like that'. Answering it turned out to be mostly photography discipline, which is not a screen you can draw in Figma."]),
),


"villey": dict(
  headline="Giving instructions to a farm you will never stand in: Villey",
  sub="A platform of virtual farms mapped onto real ones in Africa \u2014 the owner reads the farm\u2019s condition from a dashboard, issues the work, and decides what happens at harvest.",
  role="UX/UI Designer", timeline="2021", team="Hackathon team \u2014 product, engineering",

  challenge=C(
    "The person making the decisions has never farmed, and the consequences land on somebody else\u2019s land.",
    ["Villey gives a person in a city a virtual farm that corresponds to a real one in Africa. They choose what is planted, they are told what the crop needs, they authorise the work, and at harvest they decide whether the produce comes to them or is sold.",
     "That is a strange amount of authority to hand to somebody with no agricultural knowledge, on another continent, in a different hemisphere\u2019s season. Left to invent instructions, an owner will get it wrong \u2014 and the cost of getting it wrong is a real season on real land.",
     "The pacing is brutal too. A potato takes months, and for most of that period nothing happens that a remote owner can act on. A product that only speaks at planting and harvest is a product nobody opens in between.",
     "And there is a tone problem underneath all of it. Somebody is doing this work for real. Wrapping that in badges and points is one step from turning a farmer\u2019s season into a game played by a stranger."],
    ("Opportunity", "Let the farm ask, and let the owner answer",
     "If the interface reports what the crop needs rather than offering a menu of things to do, an owner with no expertise can still make correct decisions \u2014 and the farm keeps its own authority.")),

  discovery=None,
  insight=dict(
    quote="The owner should never be inventing instructions. The farm should be asking, and the owner should be saying yes.",
    body=["That inverted the usual dashboard model. There is no command palette, no list of agricultural actions to choose between \u2014 the reminders are written as statements of need, in plain language, dated: <em>potatoes need water</em>, <em>strawberries are ready to be cultivated</em>.",
          "It puts the expertise where it actually lives, on the ground, and reduces the owner\u2019s job to the one thing they are qualified to do: decide, and commit. It also solves the pacing problem, because the state of the farm is worth looking at even on a week when there is nothing to answer."]),

  solution=dict(
    lead="A shelf of plants, a farm you can look at, and two lists that behave differently.",
    body=["The signed-in home is one screen: the plants along the top with their growth percentage, stewardship and badges on the left, dated reminders in the middle, and a live picture of the farm with the notification log beneath it.",
          "Ripeness interrupts \u2014 a plant at a hundred per cent opens a modal with the crop drawn large and exactly two things to do with it. Everything else is designed to be read rather than operated."],
    decisions=[
      ("The home screen is a shelf of plants",
       "Each with a growth percentage; empty slots named for what could go in them.",
       ["A plant card shows an illustration and a number \u2014 strawberry 29%, potato 100% \u2014 and that number is the whole reason to open the product on a quiet week. It moves slowly, which is exactly the right reward for something about growing.",
        "The unused slots are labelled <em>Add herbs</em>, <em>Add lettuce</em>, <em>Add raspberry</em> rather than left blank, so the empty state is the catalogue. <em>Harvest all</em> sits at the end for the week when several come good at once."]),
      ("Ripe means exactly two choices",
       "Harvest or Sell, on a modal with the crop drawn large.",
       ["This is the moment the whole season has been building to and it is a real decision about real produce, so it gets a full interruption with one object on it: a potato, a sentence, and two buttons.",
        "Offering <em>Sell</em> beside <em>Harvest</em> is what makes the model work at distance. Somebody who took on a crop in March may not want fifteen kilos shipped from another continent in September, and a plant they can convert is a plant they will plant again."]),
      ("The farm is a picture, and the picture is the report",
       "An isometric view of the real plot, opened from a thumbnail.",
       ["The owner will never visit, so the only honest way to say <em>this is what your land looks like now</em> is to draw it. Nothing in the scene is scenery \u2014 rows are dense while a crop is standing and cut to stubble afterwards, and the ground shifts from green to khaki as the season turns.",
        "A chart would have been faster to build and would have told a non-farmer nothing. A field is a thing people already know how to read, and the whole-image colour change is a status signal you can register from across a room."]),
      ("The proposition is one sentence",
       "\u2018Plant, take care and get healthy fruits and vegetables from the actual farmer to your doorstep.\u2019",
       ["A model this unusual cannot be explained by a headline of three words. The landing page spends a full sentence naming all four steps in order, because a visitor who guesses wrong \u2014 that this is a delivery box, or a farming game \u2014 is lost either way.",
        "<em>Enter your Villey</em> as the call to action does the rest. It implies a place that already exists and is yours, which is a more accurate description of the product than <em>Sign up</em>."]),
      ("Show the labour, and put people in it",
       "Six isometric tiles of actual farm work.",
       ["Ploughing, baling, cutting, loading, packing, picking \u2014 with a person in every single one. The alternative was photography of vegetables in a basket, which sells a mood and conceals the only fact that matters: somebody is doing this on your behalf.",
        "On a product where the owner is remote and the work is not, hiding the workers would have been the easy and the wrong decision. The illustration style is the same one used for the farm view, so the marketing page and the product are visibly the same thing."]),
      ("Two auth screens that are obviously one screen",
       "Log in is sign-up with the fields removed.",
       ["Same centred column, same rules top and bottom, same teal button, same quiet <em>Back</em>. Sign-up adds a name, a password confirmation and a Google shortcut; nothing else moves.",
        "The cross-link sits under the rule on both, so somebody who landed on the wrong one is one click from the right one rather than back at the navigation."]),
      ("The farm asks; the owner answers",
       "Dated cards you act on, and a plain log you scan.",
       ["A reminder is a request with a date on it \u2014 <em>potatoes need water, 12.11.2020</em> \u2014 and gets a card with an illustration of the task, because something is being asked of you. A notification is a fact \u2014 <em>potato is good quality</em>, <em>customers for potato are here</em> \u2014 and gets a single line.",
        "Merging them would have buried the three things that need a decision under everything that merely happened. Splitting them also draws the line the whole product depends on: what the farm needs from you, and what the farm is telling you."]),
      ("Score the stewardship, not the yield",
       "A ring at 74%, a badge, and a line of encouragement.",
       ["The number rates how well the owner has kept up with what the farm asked \u2014 not how much was produced. The yield belongs to the people working the land, and turning their output into a stranger\u2019s personal score would be dishonest about who did the work.",
        "It is the lightest possible gamification on purpose: one ring, one badge, an XP figure and an invitation to bring in neighbours. Anything more would have made a real season on real land look like a game about one, which is the failure mode this product has to stay furthest from."]),
    ]),

  outcome=dict(
    lead="A season directed from a desk, with the expertise left where it belongs.",
    body=["Villey came out of Garage48 as a full flow: a landing page that explains an unfamiliar model in one sentence, sign-up, a dashboard built for the long middle of the season, a drawn farm that reports its own state, and a harvest that ends in a real decision.",
          "The structural bet \u2014 that the farm should ask and the owner should only answer \u2014 is what let somebody with no agricultural knowledge hold genuine authority without doing damage with it."]),

  reflection=dict(
    title="What I would keep, and what I would want to fix",
    body=["Designing for the empty weeks rather than the eventful ones is the lesson I would take anywhere with a long cycle in it. The exciting screen mostly designs itself; the product lives or dies in the period where nothing is happening.",
          "The part I would push on is the other end of the relationship. Every screen here is built for the owner, and the farmer appears only as work being illustrated. A real version needs a surface where the people on the ground can say something back \u2014 raise a problem, refuse an instruction, show what actually happened \u2014 otherwise the product is a very well-designed one-way mirror."]),
),

"veon": dict(
  headline="The same two numbers, on four different backgrounds: VEON",
  sub="A chart and table component set for a seven-market telecom group \u2014 built so one figure looks like itself in a report, a deck, a press release and a web page.",
  role="UX/UI Designer", timeline="2020", team="Client, brand",

  challenge=C(
    "A listed group publishes the same figure a dozen times, and it is redrawn every time.",
    ["VEON operates across Russia, Pakistan, Algeria, Bangladesh, Ukraine, Uzbekistan and Kazakhstan. A metric like 4G network coverage is therefore never one number \u2014 it is seven series, quarter by quarter, and it appears in results announcements, investor decks, the annual report and the corporate site.",
     "Each of those surfaces has a different background. The report page is white, the deck is dark, the campaign layout is brand yellow, the web section is light grey. A chart designed for one of them fails on the other three, so in practice somebody rebuilds it.",
     "Rebuilding is where the inconsistency comes from \u2014 different colours per market, different quarter labels, gridlines that survive on screen and vanish on a projector, and a source line that is sometimes there and sometimes not.",
     "For a company on two stock exchanges, that last one is not a cosmetic problem. A figure without a source and a date is a compliance question, not a design preference."],
    ("Opportunity", "Fix the geometry, vary only the surface",
     "If the structure, colour assignments and label rules are decided once, every context becomes a theme rather than a redraw.")),

  discovery=None,
  insight=dict(
    quote="The design problem was not the chart. It was that the chart had to be recognisable four times.",
    body=["Consistency across surfaces is what makes a series of quarterly figures readable as a trend rather than as unrelated pictures. Somebody who saw the coverage chart in the deck should recognise it in the report without re-reading the legend.",
          "So the work was a single geometry \u2014 the same order of markets, the same colour per market, the same axis and label treatment \u2014 with four surface treatments applied over it, rather than four charts that happen to show the same data."]),

  solution=dict(
    lead="One table and one chart, each in four themes, sharing a colour key.",
    body=["The table lists markets as rows and quarters as columns, with percentages right-aligned and a flag carrying the row. The chart plots the same markets as lines against the same quarters, with a legend that repeats the table\u2019s order and colours.",
          "Both exist as light, grey, dark and brand-yellow variants. Nothing moves between them except the surface: the same rows in the same order, the same series in the same colours."],
    decisions=[
      ("The flag carries the row",
       "A country mark instead of a repeated name column.",
       ["In a seven-market table read across eight quarters, the eye returns to the row label constantly. A flag is recognised faster than a word and does not change length between languages, which matters on a document published in more than one.",
        "The name stays beside it rather than being replaced by it. A flag alone is a quiz for anybody outside the region, and this is a document for investors as much as for staff."]),
      ("One line per market, and the legend is the key to everything",
       "Fixed colours, fixed order, dots at every quarter.",
       ["The colour assigned to a market is the same in the chart, the legend and the table, so a reader learns the key once and carries it through a whole report. Assigning colours per chart is the single most common way this goes wrong.",
        "Every quarter gets a visible dot rather than a smooth line. These are eight discrete measurements, not a continuous signal, and drawing them as points connected by lines is the honest representation of that."]),
      ("Four themes, one geometry",
       "Light, grey, dark and brand yellow \u2014 nothing else changes.",
       ["Column widths, row heights, type sizes, axis spacing and label positions are identical across all four. Only the surface, the rule colour and the text contrast move, which is what makes the same chart recognisable on a slide and on a page.",
        "The brand-yellow variant is the constrained one and was designed first. If the component survives being set on a saturated ground, the white and grey versions are free."]),
      ("Bands instead of gridlines for the projected version",
       "Alternating vertical column bands on the dark theme.",
       ["Fine horizontal gridlines are the first thing a projector loses, and a chart with no reference marks is a picture of a slope. Wide alternating bands behind the quarters survive projection and low contrast, and they band the axis a reader is actually tracking along.",
        "It is the one place where the geometry is allowed to differ, because the failure mode it fixes only exists in that context."]),
      ("A table of fifty numbers needs a way to point",
       "One cell highlighted, in the theme\u2019s accent.",
       ["Seven rows by eight columns is more than anybody reads. The highlight exists so a presenter or a caption can say <em>this one</em> \u2014 without bolding, colouring or otherwise reformatting the surrounding data to make it stand out.",
        "It is a single cell state rather than a row or column, because the claim being made is almost always about one market in one quarter."]),
      ("The source line is part of the component",
       "Source and date sit under every chart and every table, always.",
       ["On a listed company an unsourced figure is a problem rather than an untidiness, so the attribution is built into the component instead of being left to whoever assembles the page.",
        "It is set small and low-contrast so it never competes with the data, but it cannot be omitted \u2014 the component simply does not have a version without it. That is the most reliable way to make a rule hold across a large organisation."]),
    ]),

  outcome=dict(
    lead="A figure that stays the same figure wherever it is published.",
    body=["Two metrics across seven markets and eight quarters, rendered as a table and a chart, each available in four surface treatments that share one geometry and one colour key.",
          "Because the variants differ only in surface, anybody assembling a deck or a page picks a theme rather than redrawing a chart \u2014 and the source line comes with it."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Designing the hardest-constrained variant first is a habit worth keeping. The yellow version had the least contrast to work with, and solving it made the other three fall out almost for free \u2014 the reverse order would have produced three good charts and one compromise.",
          "Building the source line into the component rather than documenting it as a rule is the other. Guidelines get skipped under deadline; a component that has no version without an attribution line does not."]),
),

"barlepie": dict(
  headline="Charts as a product, not a feature: Barlepie",
  sub="A library of chart templates a team can style, fill with their own data and embed \u2014 without a designer or a front-end developer.",
  role="UX/UI Designer", timeline="2021", team="Client, engineering",

  challenge=C(
    "Everybody needs a chart on their site and almost nobody has the two people it normally takes.",
    ["Putting a decent bar chart on a marketing page usually means a designer to make it fit the brand and a developer to wire it to the data. For a small team that is a week of two people's time for one graphic.",
     "The alternative most teams reach for \u2014 a screenshot from a spreadsheet \u2014 is unstyled, unreadable on a phone and out of date the moment the numbers change.",
     "A template library only solves that if the templates are genuinely good by default. A chart that needs work before it looks right has not saved anybody anything."],
    ("Opportunity", "Design the defaults, not the options",
     "The value is in what the chart looks like before anyone touches it. Customisation is the escape hatch, not the product.")),

  discovery=None,
  insight=dict(
    quote="Nobody wants a chart builder. They want a chart, and to stop thinking about it.",
    body=["Tools in this space compete on how much you can configure, which is exactly backwards for the person who has one number to publish this afternoon.",
          "So the flow is upload, pick a template, adjust the few things that matter \u2014 colour, type, labels \u2014 and take the embed code. Everything else has an opinion baked in."]),

  solution=dict(
    lead="A catalogue of finished charts, each of which happens to be editable.",
    body=["Bar, line, pie, scatter and their relatives, each designed to be legible at the sizes people actually publish at rather than at poster scale. Data arrives as CSV, Excel or JSON, or from a live source that keeps the chart current after publication.",
          "Customisation is limited to the decisions a non-designer can get right: palette, typeface, data labels. The proportions, spacing, axis treatment and small-screen behaviour are not exposed, because those are where an untrained hand does the most damage."],
    decisions=[
      ("Templates that are finished, not starting points",
       "Every chart is publishable the moment your data is in it.",
       ["The default state of each template is the design work. Legibility, contrast, label density and how the chart behaves on a phone are decided once, properly, so the user inherits them instead of negotiating them.",
        "That is also what makes the library a product rather than a toolkit \u2014 the promise is a good chart in two minutes, and every configuration option added is a way for that promise to fail."]),
      ("Embed is the finish line",
       "A snippet you paste, that keeps updating.",
       ["The whole journey ends in somebody else's website, so the export is the feature. Connecting a live source means the chart is still right a month later, which is where a pasted screenshot always loses.",
        "Annotations and comments sit with the chart rather than around it, so the story the numbers are telling travels with them into wherever they end up."]),
    ]),

  outcome=dict(
    lead="A chart on the page by lunchtime.",
    body=["Teams with no designer and no front-end capacity can publish charts that look designed, stay current and read properly on a phone.",
          "The library holds its consistency because the parts that carry it \u2014 spacing, axis language, label behaviour \u2014 were never made configurable in the first place."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Restricting what a user can change is usually framed as a limitation. Here it was the entire value proposition, and the hardest part was persuading everyone that fewer controls was the feature.",
          "Charts are also a good reminder that defaults are design. Most people never open the settings, so whatever the tool does on its own is what the tool is."]),
),

"11-corners": dict(
  headline="Selling a season, sorting by trust: 11 Corners",
  sub="A Georgian tour marketplace \u2014 twelve hundred trips from operators nobody abroad has heard of, sold to travellers who have not decided where they are going yet.",
  role="UX/UI Designer", timeline="2021", team="Client, engineering",

  challenge=C(
    "Neither the platform nor the operators on it have a reputation to trade on.",
    ["11 Corners aggregates tours from small Georgian operators: wine trips in Kakheti, day trips to Kazbegi, walks in old Tbilisi. Twelve hundred of them, from companies a foreign traveller has no way to evaluate and a brand they have never heard of either.",
     "The traveller is also not where a booking engine assumes they are. Somebody typing a hotel name has decided; somebody looking at Georgia in February has not decided the country, the region or the month, and a form with four empty fields is no help to them.",
     "So the funnel is upside down. The interesting work is above the search box \u2014 giving a person a reason to want a place \u2014 while the search box still has to be there for the minority who arrived knowing.",
     "And a marketplace cannot vouch for its own inventory. Any \u2018recommended\u2019 ordering is a claim about operators the platform has not verified, and if it is wrong once it costs the traveller a day of their holiday."],
    ("Opportunity", "Borrow the country\u2019s reputation, then lend it back",
     "Sell Georgia editorially at the top of the funnel, and make the ordering of results something a traveller can audit rather than something they have to take on faith.")),

  discovery=None,
  insight=dict(
    quote="A tour company nobody has heard of cannot sell itself. It can sell Georgia in February, and let the ratings do the rest.",
    body=["The home page therefore opens on a season rather than a search \u2014 <em>Spend Winter in Georgia</em> over a photograph of the mountains, with the search fields laid across the bottom of it for anyone who does not need persuading.",
          "Everything below that is a different way of answering \u2018where should I go\u2019: offers, tours picked for you, one destination given the full width, and a blog. The catalogue itself is the last thing a visitor meets, not the first."]),

  solution=dict(
    lead="Editorial at the top, an auditable catalogue underneath, and one card component throughout.",
    body=["The home page runs a seasonal hero with a four-field search laid over it, three plain reassurances, two tour carousels, a full-width destination feature and a row of articles. The listing page keeps the same search bar pinned above the results with an advanced-search toggle, because travel search is iterative rather than a single query.",
          "The tour card is one component used everywhere \u2014 in the home carousels, in the listing grid, and at the foot of a blog post \u2014 so a small team maintains one thing and the traveller learns one object."],
    decisions=[
      ("Open on a season, not a search box",
       "\u2018Spend Winter in Georgia\u2019, with the search fields laid across the photograph.",
       ["A search form as the hero assumes a decision the visitor has not made. Naming a season instead gives somebody a reason to be here before asking them to specify anything, and it is content the platform can change four times a year without a redesign.",
        "The fields still sit on the hero rather than a screen below, so the person who does know what they want has lost nothing. Underneath, three plain reassurances \u2014 wide selection, easy payment, happy customers \u2014 answer the first three doubts about an unfamiliar booking site before any tour is shown."]),
      ("Two carousels that mean different things",
       "Special Offers, then Tours For You.",
       ["One row is priced \u2014 discounted trips, with the old figure struck through \u2014 and the other is chosen. Merging them into a single \u2018featured\u2019 rail would have made both meaningless, because a traveller reads a discount and a recommendation completely differently.",
        "Both are carousels rather than grids so the page stays scannable at full height. On a home page whose job is to give reasons, a visitor should reach the bottom of it."]),
      ("One destination gets the whole width",
       "A full-bleed card: <em>Top Destination \u2014 Kazbegi \u2014 See Tours</em>.",
       ["Between two rows of identical cards, one place is given a photograph large enough to actually want. It is the only module on the page that sells a location rather than a product, and it is what turns a browse into a search.",
        "It is a slider, so the featured destination rotates without the layout changing \u2014 the same editorial slot works in every season."]),
      ("Put the articles on the home page",
       "Three posts, in the same rhythm as the tours.",
       ["Somebody who has not chosen a country will read before they book. Putting the blog on the home page rather than behind a nav item treats reading as part of the funnel instead of as content marketing filed elsewhere.",
        "The cards use the same proportions as the tour cards, so the page has one rhythm and the articles read as part of the offer rather than as a separate publication."]),
      ("Twelve hundred results, and only two ways to sort",
       "\u2018Top Rated Tours \u2014 1,200 Results\u2019, sorted by rating or by price.",
       ["The count is stated because on a marketplace it is reassurance rather than a warning: twelve hundred trips means the answer is probably in here.",
        "There is deliberately no \u2018recommended\u2019 option. A marketplace that has not vetted its operators cannot honestly promote one over another, and rating and price are the two orderings a traveller can check for themselves. Removing the third one removes the only sort that could quietly be sold."]),
      ("One card, and a ribbon when the client needs one",
       "The same tour card everywhere, with a \u2018Special Destination\u2019 flag on some.",
       ["Photograph, title, one line of description, a price chip. The identical component appears in the home carousels, the listing grid and under a blog post, which keeps the build small and means a traveller learns the object once.",
        "Merchandising is handled by a corner ribbon rather than by a different card. It gives the client somewhere to promote without letting promotion distort the grid \u2014 the flagged tour is still directly comparable with the ones beside it."]),
      ("The About page is built from the home page",
       "The same reassurances, offers, tours and articles, under a paragraph.",
       ["A traveller reaches About because they are unsure, and the honest answer to that is not more prose \u2014 it is the reassurances again and then the actual inventory. The page states who the company is and immediately resumes selling.",
        "It is also the maintenance argument. Composing it from modules that already exist means a two-person team never has a page that quietly goes stale, and there is no second layout to keep in step."]),
      ("An article is a page, not a post",
       "A wide single column, inline photographs with captions, and sharing in the margin.",
       ["The reading experience is given the full treatment \u2014 generous measure, images that break the text at their own scale, captions in their own voice. If reading is part of the funnel then a cramped blog template is a leak in it.",
        "Author and date sit at the top with the share controls beside them rather than at the end, because on travel content the decision to send an article to whoever you are travelling with happens while reading it."]),
      ("The article ends in tours",
       "More reading, and then Similar Tours.",
       ["Every post closes with two rows: other articles for somebody still exploring, and bookable trips for somebody who has just been convinced. The second row is the whole reason the blog exists.",
        "They are in that order on purpose. Leading with tours would make the article read as an advert, which is exactly what stops it working."]),
    ]),

  outcome=dict(
    lead="A marketplace that argues before it asks.",
    body=["The platform sells a season, then a destination, then an article, and only then a catalogue \u2014 with twelve hundred tours ordered by two things a traveller can verify.",
          "One card component carries the inventory across every surface, and the About page is assembled from the same modules, which is what makes a catalogue this size maintainable by a small team."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Refusing to build a \u2018recommended\u2019 sort is the decision I would defend hardest. It is the one every marketplace adds and the one that quietly turns a ranking into inventory to be sold \u2014 and on a product where a bad result costs somebody a day of their holiday, that trade is not worth making.",
          "Leading with a season rather than a search box is the other. It dates the home page on purpose, which sounds like a liability and is actually the thing that makes it worth returning to."]),
),

"tales": dict(
  headline="Folklore has no index, so we built three: Tales with Tails",
  sub="An archive of Georgian myths, legends and sacred places \u2014 collected from the people who live near them, and findable by map, by region or by word.",
  role="UX/UI Designer", timeline="2022", team="Editors, engineering",

  challenge=C(
    "A legend has no author, no date and no category \u2014 which is everything a normal archive is filed by.",
    ["Georgian folklore is enormous and almost entirely oral. A story about Kopala belongs to Pshav-Khevsureti; a spirit belongs to a particular pass or spring. There is no publication date, usually no writer, and frequently several incompatible versions of the same tale.",
     "Every filing system a website reaches for by default therefore fails. Newest-first is meaningless for a story two centuries old. Alphabetical assumes you know the name. A flat category list flattens the one thing that actually distinguishes these stories, which is where they come from.",
     "There is a tone trap on either side. Treat this material academically and it becomes a museum nobody browses; treat it decoratively and it becomes tourist-board folklore, which is an insult to the people it was collected from.",
     "And the archive only survives if it keeps growing \u2014 which means asking strangers to contribute stories they heard from a grandparent, without making that feel like submitting to a journal."],
    ("Opportunity", "Index by place, and let the illustration carry the tone",
     "Place is the one attribute every legend genuinely has. Build the navigation on it, and spend the design effort on making a body of oral history look like something worth reading.")),

  discovery=None,
  insight=dict(
    quote="Nobody looks for a legend by name. They look for the one from the place they are from.",
    body=["That reframed the entire information architecture. The primary questions are <em>what happened near here</em> and <em>what does my region have</em>, not <em>what is the most recent story</em>.",
          "So there are three parallel ways in, none of them a hierarchy: a map with pins for anyone thinking geographically, a grid of Georgian region silhouettes for anyone thinking administratively, and a field of words for anyone who half-remembers a creature but not where it lived."]),

  solution=dict(
    lead="Three doors into one archive, in a collage that treats folklore as strange rather than quaint.",
    body=["The home page runs from a collaged hero into featured stories laid out like a magazine, then hands over to the three finding tools in sequence: filter on a map, pick a region silhouette, or scan a field of words. A separate stories index adds search, dropdown filters and removable chips for anyone who wants to work at it.",
          "The visual language is Victorian engravings \u2014 a dodo, a spider, a winged cow, a sphinx \u2014 cut against photographic fragments and flat blocks of coral, teal and yellow."],
    decisions=[
      ("Engravings instead of illustrations of monsters",
       "Nineteenth-century natural-history prints, collaged with photography and flat colour.",
       ["You cannot photograph a myth, and drawn dragons would have turned the archive into fantasy. Antique scientific engravings solve it exactly: they are strange, they are old, and they were made by people who believed they were documenting something real \u2014 which is the same posture as the stories.",
        "Cutting them against photographic fragments and flat geometry keeps the result from reading as heritage design. The material is treated as unsettling rather than charming, because that is what it is."]),
      ("The featured stories read like a magazine",
       "Image left, then image right, alternating down the page.",
       ["A grid says <em>catalogue</em>; an alternating spread says <em>read this one</em>. On a home page whose job is to make somebody start a story rather than survey the archive, three large entries beat twelve small ones.",
        "Each block carries the title, its tags, an excerpt and a footer of likes, comments and shares. Those metrics are unusual on a folklore archive and they are deliberate \u2014 they are the only evidence a visitor has that other people are here too."]),
      ("Filtering by region sits next to an actual map",
       "A form on the left, a live map on the right, one pin at a time.",
       ["Region names mean little to a visitor who is not Georgian, so the filter is paired with the map rather than standing alone. Choosing in the list moves the pin; the two halves teach each other.",
        "It is the practical counterpart to the region grid further down \u2014 the same question answered once for somebody who knows the country and once for somebody who does not."]),
      ("The project explains itself in the middle, not at the top",
       "A dark band with an engraving, halfway down the home page.",
       ["An <em>about the project</em> section above the content is a paragraph nobody reads. Placing it after the first stories means it is met by somebody who has already seen what this is and now wants to know who made it.",
        "Inverting to near-black separates it from the archive around it without a heading having to do that work, and it gives the engravings their strongest contrast on the whole site."]),
      ("Regions are drawn, not listed",
       "A grid of actual Georgian region outlines, each named.",
       ["A dropdown of twelve region names is a form control. Twelve silhouettes are a map you can read at a glance \u2014 and for a Georgian visitor their own region\u2019s shape is recognised before the label is.",
        "Rendering them as flat shapes rather than one interactive map also means the choice works on a phone, where a pannable map of a whole country is close to unusable. The region with stories in it fills with a texture; the rest stay grey."]),
      ("A field of words for the half-remembered",
       "Around thirty terms, laid out as a block on dark.",
       ["The most common way somebody arrives at folklore is with a fragment \u2014 a creature, a rite, a word a grandparent used. Neither a map nor a region helps with that, so the third door is simply the vocabulary itself.",
        "It is set as an even field rather than a weighted tag cloud. Sizing words by frequency would suggest some legends matter more, which is the opposite of what an archive should imply."]),
      ("Filters you can see and take off",
       "Dropdowns that deposit removable chips above the results.",
       ["With several overlapping taxonomies \u2014 region, category, creature \u2014 the common failure is a visitor who has narrowed to nothing and cannot tell why. Chips make the current query visible as objects, each with its own cross.",
        "It matters more here than on a shop, because a folklore query returns nothing far more often than a product search does."]),
      ("Two columns, thirty-six pages, and a card that stays quiet",
       "Photograph, category, title, excerpt, tags, and a footer of counts.",
       ["The index runs to thirty-six pages, so the card had to survive being seen a hundred times. Two columns rather than three keeps the photograph large enough to be the reason somebody clicks.",
        "Everything else on the card is set small and grey. The image argues, the text confirms \u2014 which is the same order in which somebody decides to read a story."]),
      ("The map page asks for the next story",
       "Pins with counts, and \u2018share your story\u2019 underneath.",
       ["Pins carry the number of legends at that location, so the map doubles as a coverage report: it shows where the archive is thin as clearly as where it is rich.",
        "That is exactly why the invitation to contribute sits directly beneath it, with its own artwork and its own button. The moment somebody notices their own region has almost nothing on it is the moment they are most likely to write something."]),
      ("A story ends somewhere, not nowhere",
       "Counts, then a carousel of similar stories.",
       ["Archive sites lose people at the bottom of an article, because a finished story is a finished visit. Related stories sit immediately under the text, drawn from the same tags, so reading one legend begins a session rather than ending one.",
        "The like, comment and share counts sit between the two, at the point where somebody has just finished and is deciding what this was worth."]),
    ]),

  outcome=dict(
    lead="An archive organised the way the material actually behaves.",
    body=["Stories are found by pin, by region or by word, read on a page that leads to another one, and added by the people who grew up with them \u2014 with the map showing where the gaps still are.",
          "The collage identity \u2014 engravings, photographic fragments and flat colour \u2014 gave a body of oral history a contemporary surface without flattening what is strange about it, and it carries through to the phone, where the menu becomes a full-screen panel with an engraving in the corner."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Building navigation on the one attribute the content genuinely has, rather than the ones a CMS supplies by default, is the decision I would repeat on any archive. Date and category were both available and both would have been wrong.",
          "The illustration direction did more work than any layout choice. Deciding what a subject should feel like, and then finding a visual tradition that already carries that feeling, settles a hundred smaller decisions that would otherwise be argued one at a time."]),
),

"mult-georgia": dict(
  headline="A shopping centre that happens to be a website: Mult Georgia",
  sub="A Georgian multi-vendor marketplace \u2014 groceries, cosmetics, electronics, clothing, toys and licensed brands \u2014 where anybody can open a shop and every category shops differently.",
  role="UX/UI Designer", timeline="2021", team="Client, engineering",

  challenge=C(
    "Selling everything means every category is decided differently, and none of the sellers are you.",
    ["Mult is not a retailer with a wide catalogue \u2014 it is a marketplace. The masthead carries \u2018Sell with us\u2019 next to the logo, which means the catalogue is assembled by hundreds of independent merchants rather than a buying team.",
     "A Samsung Galaxy is chosen from a fifteen-row specification table. A leather bag is chosen from photographs. Household chemicals are chosen by brand and price and nothing else. One product template cannot serve all three without failing at least two.",
     "Marketplaces also have a photography problem that single-brand shops do not. Every merchant shoots their own product, so the grid is a collision of studio cut-outs, phone snaps and stock imagery \u2014 and no amount of guidelines fixes what has already been uploaded.",
     "And nothing on the site is a household name. A shopper who has never heard of the seller, on a platform that sells vegetables next to smartphones, needs a reason to believe an order will arrive."],
    ("Opportunity", "Borrow the credibility of a real shopping centre",
     "Georgians already trust the mall. If the site reads as a building with named shops inside it rather than an infinite database, the unfamiliar seller inherits the frame.")),

  discovery=None,
  insight=dict(
    quote="A marketplace has no products of its own. What it can design is the shelf they sit on.",
    body=["That reframed almost every decision. The platform does not control the photography, the descriptions or the pricing \u2014 so the design work is the container: how a card holds a bad photo and a good one equally well, how a specification table renders whatever a merchant typed into it, how a category communicates before a single product is seen.",
          "It is also why the category pages are illustrated with photographs of real retail interiors \u2014 a mall atrium, a clothing rail, a grocery aisle. They set an expectation that no merchant\u2019s own imagery could, and they do it before the catalogue can undermine it."]),

  solution=dict(
    lead="One shell, category-aware pages, and a shelf that flatters uneven stock.",
    body=["The header is a single row: brand, \u2018Sell with us\u2019, a search field with a category scope beside it, sign-in and the basket. Underneath, the whole catalogue hangs off one \u2018All categories\u2019 control rather than a tree competing for the top of the page.",
          "Browsing runs through category cards, discounts and best-sellers, with a dark editorial band for partner brands. Filtering is a plain left rail \u2014 category checkboxes, a discount toggle, a price range \u2014 identical everywhere so it is learned once. The product page changes shape by category: a specification table for electronics, imagery and zoom for anything chosen by eye."],
    decisions=[
      ("Category cards break the banner, on purpose",
       "Shortcut cards overlap the hero carousel rather than sitting below it.",
       ["A promotional banner is the least useful thing on a marketplace home page and it always takes the best position. Letting the category cards overlap its lower half puts navigation in the first screen without giving up the campaign slot.",
        "It also fixes a scanning problem. Four white cards on a saturated photograph are the highest-contrast object on the page, so the eye lands on the route into the catalogue rather than on the advert."]),
      ("Every product card is a small gallery",
       "Dots inside the card, swipeable in the grid.",
       ["On a marketplace the first photograph is whatever the merchant uploaded first, and it is frequently the worst one. Letting a shopper cycle images without opening the product rescues listings that a single thumbnail would have killed.",
        "The cost is a busier card, so everything else on it was cut back to four elements: image, title, hashtags, price. The discount badge is a soft pink circle rather than a red flash \u2014 frequent enough on this platform that it cannot be allowed to shout."]),
      ("Categories are photographed as places, not products",
       "A mall atrium, a clothing rail, a grocery aisle.",
       ["Product cut-outs on a category card promise a specific item and deliver a list. A photograph of a shop promises a section of a building, which is exactly what a category is \u2014 and it is imagery the platform owns rather than imagery a merchant supplied.",
        "It carries the central metaphor without a word of copy. Mult reads as a shopping centre you walk into, which is a familiar and forgiving frame for a stranger\u2019s stall."]),
      ("Search scopes before it searches",
       "A category selector inside the search field.",
       ["\u2018Apple\u2019 on this platform is a phone, a fruit and a phone case. Scoping the query before it runs removes an entire class of useless result set, and it costs one dropdown in a control people already look at.",
        "Searching everything returns categories rather than a flat list, so a vague query lands somewhere navigable instead of on page one of nine hundred."]),
      ("Filters stay in the same rail whatever changes inside them",
       "Category checkboxes, a discount toggle, a price range.",
       ["The facets differ by section, but the rail does not move, relabel or reorder. A shopper who filtered trainers last week finds groceries the same way, which is the only thing making a catalogue this wide learnable.",
        "The set is deliberately short. Long facet lists are built for buyers who know the vocabulary of a category, and on a general marketplace most shoppers do not."]),
      ("Specifications are a table, not prose",
       "Fifteen zebra-striped rows, label left, value right.",
       ["An electronics buyer is comparing across tabs, and comparison needs a fixed row order. The table takes whatever a merchant filled in and renders it identically for every phone on the platform.",
        "Anything a merchant wants to say in their own voice goes above it, in the description. Separating the two means bad copy cannot contaminate the part being compared."]),
      ("Zoom on the page, lightbox off it",
       "A magnifier lens inline; a full-screen view with the buy panel still attached.",
       ["Marketplace photography is inconsistent, so the shopper has to inspect it \u2014 stitching, screen bezel, print quality. The inline lens answers that without leaving the page or losing the price.",
        "Opening the image fully keeps the thumbnail rail and the purchase panel visible, so the moment inspection is satisfied the decision can be made without navigating back."]),
      ("Bundles are shown as an equation",
       "Product plus product equals a total, with quick-buy and add-to-basket.",
       ["\u2018Also bought\u2019 usually means a carousel that nobody reads. Rendering it literally \u2014 headphones + cable = 2 items, 245 GEL \u2014 makes the offer legible in a second.",
        "Two commitments are offered because they are different intentions: buy this pair now, or add it and keep shopping. Collapsing them into one button loses whichever shopper it was not built for."]),
      ("Partner brands get an editorial band, not a shelf",
       "A dark section with a mosaic of brand stories.",
       ["When a real brand joins a marketplace of unknowns, that is the platform's strongest trust signal and it deserves to look nothing like a product row. The band inverts to dark and switches to a mosaic so it reads as an announcement.",
        "The cards carry a line about the brand and where to see the collection rather than a price, because at that moment the platform is selling its own credibility rather than an item."]),
    ]),

  outcome=dict(
    lead="A wide, seller-supplied catalogue that stays navigable and does not look assembled.",
    body=["Groceries, cosmetics, electronics, clothing, toys and licensed brands sit in one shell with one filter rail, one card grammar and a product page that changes shape according to what is being decided.",
          "Because the container carries the quality, the platform can absorb a merchant with poor photography or thin copy without the whole grid degrading \u2014 which on a marketplace is the difference between growing the catalogue and diluting it."]),

  reflection=dict(
    title="What I would keep from this one",
    body=["Designing for content you do not control is a different discipline from designing for content you do. The useful question stops being \u2018how should this look\u2019 and becomes \u2018how badly can this be filled in before it breaks\u2019 \u2014 and the answer shapes the component more than any layout preference.",
          "Borrowing a familiar physical metaphor did more for trust than any badge or guarantee would have. The mall photography is the cheapest decision in the project and probably the one that carried the most weight."]),
),
}
