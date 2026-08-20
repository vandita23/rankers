-- KisanAI MVP schema — run this in the Supabase SQL editor.
-- No auth/user tables: the frontend has no login flow yet, so this is a
-- single demo-farmer setup. Add auth tables later if the frontend needs it.

create table if not exists farmers (
    id serial primary key,
    name text not null,
    name_hi text,
    location text not null,
    location_hi text,
    crops text[] not null default '{}',
    crops_hi text[] not null default '{}',
    created_at timestamptz not null default now()
);

create table if not exists alerts (
    id serial primary key,
    farmer_id integer references farmers(id) on delete cascade,
    level text not null check (level in ('info', 'warning')),
    text_en text not null,
    text_hi text,
    created_at timestamptz not null default now()
);

create table if not exists action_items (
    id serial primary key,
    farmer_id integer references farmers(id) on delete cascade,
    text_en text not null,
    text_hi text,
    done boolean not null default false,
    created_at timestamptz not null default now()
);

create table if not exists chat_logs (
    id serial primary key,
    farmer_id integer references farmers(id) on delete set null,
    message text not null,
    language text not null default 'en',
    reply text,
    sources jsonb,
    created_at timestamptz not null default now()
);

create table if not exists disease_reports (
    id serial primary key,
    farmer_id integer references farmers(id) on delete set null,
    disease text,
    confidence integer,
    low_confidence boolean,
    language text not null default 'en',
    created_at timestamptz not null default now()
);

create table if not exists scheme_queries (
    id serial primary key,
    farmer_id integer references farmers(id) on delete set null,
    question text not null,
    language text not null default 'en',
    answer text,
    created_at timestamptz not null default now()
);

-- Seed the demo farmer (id = 1) used by GET /api/v1/dashboard.
insert into farmers (id, name, name_hi, location, location_hi, crops, crops_hi)
values (1, 'Ramesh', 'रमेश', 'Barabanki, Uttar Pradesh', 'बाराबंकी, उत्तर प्रदेश',
        array['Wheat', 'Sugarcane'], array['गेहूं', 'गन्ना'])
on conflict (id) do nothing;

insert into alerts (farmer_id, level, text_en, text_hi) values
    (1, 'warning', 'Rain expected in 2 days — delay pesticide spraying on wheat.',
     '2 दिनों में बारिश की संभावना — गेहूं पर कीटनाशक छिड़काव टालें।'),
    (1, 'info', 'PM-KISAN next installment window opens this month.',
     'PM-KISAN की अगली किस्त इस महीने आने वाली है।')
on conflict do nothing;

insert into action_items (farmer_id, text_en, text_hi, done) values
    (1, 'Delay spraying — rain expected Thursday', 'छिड़काव टालें — गुरुवार को बारिश संभव', false),
    (1, 'Check wheat leaves for yellow rust spots', 'गेहूं के पत्तों पर पीले धब्बे जांचें', false),
    (1, 'Irrigate sugarcane field (completed)', 'गन्ने के खेत की सिंचाई (पूर्ण)', true)
on conflict do nothing;
