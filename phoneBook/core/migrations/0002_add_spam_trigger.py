from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE OR REPLACE FUNCTION update_spam_stats()
                RETURNS TRIGGER AS $$
                BEGIN
                    INSERT INTO core_spamstats (target_phone, report_count, last_reported_at)
                    VALUES (NEW.target_phone, 1, NOW())
                    ON CONFLICT (target_phone)
                    DO UPDATE SET
                        report_count = core_spamstats.report_count + 1,
                        last_reported_at = NOW();
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER trigger_update_spam_stats
                AFTER INSERT ON core_spamreport
                FOR EACH ROW
                EXECUTE PROCEDURE update_spam_stats();
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS trigger_update_spam_stats ON core_spamreport;
                DROP FUNCTION IF EXISTS update_spam_stats;
            """
        ),
    ]
