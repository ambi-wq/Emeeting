from django.db import models

# Create your models here.
class Committee(models.Model):
    fid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    fn = models.CharField(max_length=200)
    stat = models.CharField(max_length=200)
    company_id = models.CharField(max_length=50)
    approved = models.CharField(max_length=20)
    inchargeid = models.CharField(max_length=50)
    presentor = models.CharField(max_length=100)

    class Meta:
        db_table = "emeet_forums"

class Meeting(models.Model):
    mid = models.CharField(max_length=200)
    dt = models.DateField()
    fid = models.IntegerField()
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    title = models.CharField(max_length=2000)
    venue = models.CharField(max_length=50)
    days = models.IntegerField()

    class Meta:
        db_table = "emeet_meeting"

############################## vedanti
class EmeetCmslogs(models.Model):
    id = models.IntegerField(primary_key=True)
    activity = models.TextField(blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    userid = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    ip = models.CharField(db_column='IP', max_length=250, blank=True, null=True)  # Field name made lowercase.
    ua = models.CharField(db_column='UA', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'emeet_cmslogs'



class EmeetForums(models.Model):
    fid = models.IntegerField()
    fname = models.CharField(max_length=200, blank=True, null=True)
    fn = models.CharField(max_length=100, blank=True, null=True)
    stat = models.CharField(max_length=10, blank=True, null=True)
    company_id = models.CharField(max_length=50, blank=True, null=True)
    approved = models.CharField(max_length=20, blank=True, null=True)
    inchargeid = models.CharField(max_length=50, blank=True, null=True)
    presentor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emeet_forums'

class EmeetAnnualMeetings(models.Model):
    id = models.IntegerField(primary_key=True)
    forum = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    dt = models.CharField(max_length=50, blank=True, null=True)
    fid = models.CharField(max_length=50, blank=True, null=True)
    venue = models.TextField(blank=True, null=True)
    company_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emeet_annual_meetings'

class EmeetMsg(models.Model):
    id = models.IntegerField(primary_key=True)
    msg = models.TextField(blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    comm = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emeet_msg'

class EmeetBoardMembers(models.Model):
    id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    desg = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    srno = models.AutoField(primary_key=True)
    company = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    qualify = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'emeet_board_members'


class EmeetApprovals(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=6, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    expiry_dt = models.DateTimeField(db_column='Expiry_dt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'emeet_approvals'


class EmeetApprovalUsers(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    userid = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=15, blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    mailsent = models.IntegerField(db_column='MailSent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'emeet_approval_users'

