import os
cwd = os.getcwd()
import sys
sys.path.append(cwd + '/src')
import pytest
from metrics_converter import MetricsConverter
from collectd.data import Data
from collectd.helper import Helper


def test_gen_tag():
    assert MetricsConverter.gen_tag('tag_key', 'tag_value') == 'tag_key=tag_value'


def test_gen_tag_empty_value():
    assert MetricsConverter.gen_tag('tag_key', '') == ''


def test_gen_tag_empty_key_exception():
    with pytest.raises(Exception) as e:
        MetricsConverter.gen_tag('', 'tag_value')

    assert 'Key for value tag_value cannot be empty' in str(e.value)


def test_gen_tag_key_word_exception():
    with pytest.raises(Exception) as e:
        MetricsConverter.gen_tag('_sourceId', 'tag_value')

    assert 'Key _sourceId (case-insensitive) must not contain reserved keywords' in str(e.value)


def test_gen_key_not_string_exception():
    with pytest.raises(Exception) as e:
        MetricsConverter.gen_tag(('tag_key', ), 'tag_value')

    assert "Field ('tag_key',) must be string type. Type is <type 'tuple'>" in str(e.value)


def test_gen_value_not_string_exception():
    with pytest.raises(Exception) as e:
        MetricsConverter.gen_tag('tag_key', 1)

    assert "Field 1 must be string type. Type is <type 'int'>" in str(e.value)


def test_tags_to_str():
    tags = ['tag_key1=tag_val1', 'tag_key2=tag_val2', 'tag_key3=tag_val3']
    tag_str = MetricsConverter.tags_to_str(tags)

    assert tag_str == 'tag_key1=tag_val1 tag_key2=tag_val2 tag_key3=tag_val3'


def test_tags_to_str_with_empty_tag():
    tags = ['tag_key1=tag_val1', '', 'tag_key3=tag_val3']
    tag_str = MetricsConverter.tags_to_str(tags)

    assert tag_str == 'tag_key1=tag_val1 tag_key3=tag_val3'


def test_tags_to_str_with_empty_tags():
    tags = []
    tag_str = MetricsConverter.tags_to_str(tags)

    assert tag_str == ''


def test_convert_to_metrics():
    d = Data()
    print 'this is data %s' % str(d.type)
    helper = Helper()
    metrics = MetricsConverter.convert_to_metrics(d, helper.conf.types)

    assert metrics == [Data.default_metric()]
