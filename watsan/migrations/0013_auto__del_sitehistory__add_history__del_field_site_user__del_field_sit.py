# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SiteHistory'
        db.delete_table('watsan_sites_history')

        # Adding model 'History'
        db.create_table('watsan_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 5, 14, 38, 12))),
        ))
        db.send_create_signal('watsan', ['History'])

        # Adding M2M table for field sites on 'History'
        db.create_table('watsan_history_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('history', models.ForeignKey(orm['watsan.history'], null=False)),
            ('site', models.ForeignKey(orm['watsan.site'], null=False))
        ))
        db.create_unique('watsan_history_sites', ['history_id', 'site_id'])

        # Deleting field 'Site.user'
        db.delete_column('watsan_sites', 'user_id')

        # Deleting field 'Site.date_added'
        db.delete_column('watsan_sites', 'date_added')

        # Adding field 'Site.method'
        db.add_column('watsan_sites', 'method',
                      self.gf('django.db.models.fields.CharField')(default='map-click', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'SiteHistory'
        db.create_table('watsan_sites_history', (
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['watsan.Site'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('watsan', ['SiteHistory'])

        # Deleting model 'History'
        db.delete_table('watsan_history')

        # Removing M2M table for field sites on 'History'
        db.delete_table('watsan_history_sites')

        # Adding field 'Site.user'
        db.add_column('watsan_sites', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Site.date_added'
        db.add_column('watsan_sites', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 1, 11, 13, 25, 3)),
                      keep_default=False)

        # Deleting field 'Site.method'
        db.delete_column('watsan_sites', 'method')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'base_map.shape': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'Shape'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'watsan.history': {
            'Meta': {'object_name': 'History'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 5, 14, 38, 49)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['watsan.Site']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'watsan.landmark': {
            'Meta': {'ordering': "['place_type', 'name']", 'object_name': 'Landmark'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 5, 14, 38, 49)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'place_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'watsan.manhole': {
            'Meta': {'object_name': 'Manhole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'watsan.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'org_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'watsan.road': {
            'Meta': {'ordering': "['name']", 'object_name': 'Road'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'road_type': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'watsan.searchresult': {
            'Meta': {'ordering': "['name']", 'object_name': 'SearchResult'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'search_engine': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'watsan.sewerline': {
            'Meta': {'ordering': "['name']", 'object_name': 'SewerLine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'watsan.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'watsan_sites'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'watsan.village': {
            'Meta': {'ordering': "['name']", 'object_name': 'Village'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'watsan.waterline': {
            'Meta': {'ordering': "['name']", 'object_name': 'WaterLine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'watsan.watsanusermeta': {
            'Meta': {'object_name': 'WatsanUserMeta', 'db_table': "'watsan_usermeta'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['watsan.Organization']"}),
            'question_1': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'question_2': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['watsan']