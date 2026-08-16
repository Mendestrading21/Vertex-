from vertex.engines import anomaly_context as AC


def _detail(with_ohlcv=True):
    close = [100 + index for index in range(40)]
    series = {'close': close}
    if with_ohlcv:
        series.update({'open': [value - 0.2 for value in close],
                       'high': [value + 0.5 for value in close],
                       'low': [value - 0.5 for value in close],
                       'volume': [1000 + index * 10 for index in range(40)]})
    return {'series': series}


def test_close_only_context_is_explicitly_limited():
    context = AC.build('TST', _detail(with_ohlcv=False))
    assert context['available'] is True
    assert context['provenance'] == 'CLOSE_ONLY'
    assert 'OHLCV complet absent' in context['limitations'][0]


def test_complete_ohlcv_enables_enriched_anomaly_context():
    context = AC.build('TST', _detail())
    assert context['available'] is True
    assert context['provenance'] == 'OHLCV_ENRICHED'
    assert isinstance(context['events'], list)
    assert 'benchmark absent' in context['limitations'][0]
