SET SCHEMA 'public';

INSERT INTO tank (name, manufactured, type, country)
VALUES
    ('BT-2', true, 'Light tank', 'Soviet Union'),
    ('BT-7', true, 'Light tank', 'Soviet Union'),
    ('M3 Stuart', true, 'Light tank', 'United States'),
    ('M5 Stuart', true, 'Light tank', 'United States'),
    ('Type 62', true, 'Light tank', 'China'),
    ('Spähpanzer Ru 251', false, 'Light tank', 'Germany'),
    ('Type 59', true, 'Main battle tank', 'China'),
    ('Type 74', true, 'Main battle tank', 'Japan'),
    ('Type 61', true, 'Main battle tank', 'Japan'),
    ('Batignolles-Chatillon Char 25T', false, 'Medium tank', 'France'),
    ('Panzer III/IV', false, 'Medium tank', 'Nazi Germany'),
    ('Panzerkampfwagen V Panther', true, 'Medium tank', 'Nazi Germany'),
    ('Leopard 1', true, 'Main battle tank', 'Germany'),
    ('Matilda II', true, 'Infrantry tank', 'United Kingdom'),
    ('Cromwell', true, 'Cruiser tank', 'United Kingdom'),
    ('M4 Sherman', true, 'Medium tank', 'United States'),
    ('Panzerkampfwagen VIII Maus', false, 'Super-heavy tank', 'Nazi Germany'),
    ('Elefant (aka Ferdinand)', true, 'Tank destroyer', 'Nazi Germany'),
    ('M10 Tank Destroyer (aka Wolverine)', true, 'Tank destroyer', 'United States'),
    ('M36 Tank Destroyer (aka Jackson)', true, 'Tank destroyer', 'United States'),
    ('M18 Hellcat', true, 'Tank destroyer', 'United States'),
    ('ISU-152', true, 'Assault gun', 'Soviet Union'),
    ('SU-152', true, 'Self-propelled howitzer', 'Soviet Union'),
    ('Tiger II', true, 'Heavy tank', 'Nazi Germany'),
    ('Tiger I', true, 'Heavy tank', 'Nazi Germany'),
    ('IS-7', false, 'Heavy tank', 'Soviet Union'),
    ('KV-1 (Kliment Voroshilov 1)', true, 'Heavy tank', 'Soviet Union'),
    ('IS-3', true, 'Heavy tank', 'Soviet Union')
ON CONFLICT (name) DO NOTHING;

INSERT INTO tank_image (tank_name, image_link)
VALUES
    ('BT-2', 'https://cdn.discordapp.com/attachments/1034333571218944041/1034334077928611861/unknown.png'),
    ('BT-7', 'https://cdn.discordapp.com/attachments/1034333571218944041/1034333940133146624/unknown.png'),
    ('M4 Sherman', 'https://cdn.discordapp.com/attachments/1034333571218944041/1034333623916167259/unknown.png'),
    ('Panzerkampfwagen VIII Maus', 'https://cdn.discordapp.com/attachments/1034333571218944041/1034339452769800284/unknown.png')
ON CONFLICT (image_link) DO NOTHING;
