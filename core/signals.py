# core/signals.py

from django.dispatch import Signal

# Define a custom signal
reset_group_admin_signal = Signal('instance')
