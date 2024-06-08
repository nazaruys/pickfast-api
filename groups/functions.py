def update_group_admin(instance):
        group = instance.admin_of
        if group is not None:
            group.admin = group.members.exclude(pk=instance.pk).first()
            group.save()
            if group.admin is None:
                group.delete()