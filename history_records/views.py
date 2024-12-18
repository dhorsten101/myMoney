from django.shortcuts import render

from history_records.models import HistoryRecord


def history_record_list(request):
    history_records = HistoryRecord.objects.order_by("-timestamp")

    labels = [record.timestamp.strftime("%Y-%m-%d") for record in history_records]
    # values = [float(record.total_value) for record in history_records]
    values = [
        float(record.total_value) if record.total_value else 0
        for record in history_records
    ]

    return render(
        request,
        "reports/history_record_list.html",
        {
            "history_records": history_records,
            "labels": labels,
            "values": values,
        },
    )
