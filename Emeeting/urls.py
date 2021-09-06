"""Emeeting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from EmeetingApp import views

urlpatterns = [
    path('showcommittee', views.showcommittee, name="showcommittee"),
    path('createcommittee/', views.createcommittee),
    path('Assignuser/', views.Assignuser),
    path('downloadCommitteedata/', views.downloadCommitteedata),
    path('updatecommitteeinfo/', views.updatecommitteeinfo),
    path('updateAssignuser/', views.updateAssignuser),

    path('manageMeeting/', views.manageMeeting, name="manageMeeting"),
    path('AddNewMeeting/', views.AddNewMeeting),
    path('Removemeeting/', views.Removemeeting),
    path('downloadAllMeetingdata/', views.downloadAllMeetingdata),
    path('Changepublishstatus/', views.Changepublishstatus),
    path('downloadforumsbasedata', views.downloadforumsbasedata),
    path('DraftMOMsite', views.DraftMOMsite,name="manageMeeting"),
    path('Draftuserstatus/<int:id>',views.Draftuserstatus),
    path('Draftusercomment/<int:id>',views.Draftusercomment),
    path('EditDraft/',views.EditDraft),
    path('Momcomments/<int:id>',views.Momcomments),
    path('DownloadReports/<int:id>',views.DownloadReports),
    path('NewDraftMOM/',views.NewDraftMOM),
    path('UpdateDraftMOM/',views.UpdateDraftMOM),
    path('DownloadMeeting/<int:id>/<str:fname>',views.DownloadMeeting),

    # path('Pushpak'Pushpak),

    path('info/<int:id>', views.info , name="manageMeeting"),
    path('updateinfo/', views.updateinfo),
    path('orderag/', views.orderag),
    path('ordersag/', views.ordersag),
    path('orderssag/', views.orderssag),
    path('reorderag/', views.reorderag),
    path('reordersag/', views.reordersag),
    path('reorderssag/', views.reorderssag),
    path('getdesc/', views.getdesc),
    path('updatedesc/', views.updatedesc),
    path('deleteagendas/', views.deleteagendas),
    path('userslist/', views.userslist),
    path('restrictlist/', views.restrictlist),
    path('attachment/<int:fid>/<int:mid>/<str:fname>', views.attachment),
    path('fetchagenda/', views.fetchagenda),
    path('updateagendas/', views.updateagendas),
    path('removefile/', views.removefile),
    path('uploadZip/', views.uploadZip),
    path('attendance', views.attendance,name="attendance"),
    path('downloadAttendanceReport/<int:fid>', views.downloadAttendanceReport),
    path('markattendance', views.markattendance),
    
    # path('manageMeeting', views.manageMeeting, name="manageMeeting"),

    # # path(-------------------Vedanti------------------------------),
    path('',views.loginpage),
    path('login',views.login),
    path('logout',views.logout),
    path('changePassword',views.changePassword),
    path('changeUserPass',views.changeUserPass),

    #path('showDashboard',views.showDashboard),
    path('manageUser', views.manageUser,name="manageUser"),
    path('manageActivityLogs', views.manageActivityLogs,name="manageActivityLogs"),
    path('downloadlogs',views.DownloadLogsdata),

    #path('assignCommittee',views.assignCommittee),
    path('assignCommitteeToUser',views.assignCommitteeToUser),
    path('enableUser/<str:user>',views.enableUser),
    path('wipeData/<str:user>',views.wipeData),
    path('regenerateUser',views.regenerateUser),
    path('resetPassword',views.resetPassword),
    path('setNewPassword',views.setNewPassword),
    path('changeAccStatus',views.changeAccStatus),

    path('addAgenda/',views.addAgenda),
    path('updatemeetinginfo',views.updatemeetinginfo),
    path('sendEmail',views.sendEmail),
    path('quickUpload',views.quickUpload),
    path('findSubAgendaDetails',views.findSubAgendaDetails),
    path('addSubAgenda',views.addSubAgenda),
    path('addSubSubAgenda',views.addSubSubAgenda),

    path('addUser',views.addUser),
    path('viewUser',views.viewUser),
    path('updateUser',views.updateUser),
    path('downloadUsers',views.downloadUsers),
    path('removeUser',views.removeUser),

    path('downloadMOM/<int:id>', views.downloadMOM),
    path('notice', views.notice),
    path('sendNoticeEmail', views.sendNoticeEmail),
    path('uploadMOM', views.uploadMOM),

    path('calender',views.calender,name="calender"),
    path('createCalenderMeeting',views.createCalenderMeeting),
    path('viewCalenderMeeting',views.viewCalenderMeeting),
    path('updateCalenderMeeting',views.updateCalenderMeeting),
    path('deleteCalenderMeeting/<int:id>',views.deleteCalenderMeeting),
    path('downloadCalenderMeeting/<int:fid>',views.downloadCalenderMeeting),
    path('notifications',views.notifications,name="notifications"),
    path('createNotification',views.createNotification),
    path('deleteNotification/<int:id>',views.deleteNotification),
    path('attendance',views.attendance,name="attendance"),
    path('downloadAttendanceReport/<int:fid>',views.downloadAttendanceReport),

    path('aboutus',views.aboutus,name="aboutus"),
    path('uploadDocumentAbtus',views.uploadDocumentAbtus),
    path('deleteAboutusDocument/<int:id>',views.deleteAboutusDocument),
    path('viewAboutUs',views.viewAboutUs),
    path('updateAboutUs',views.updateAboutUs),
    path('errorPage',views.errorPage),

    path('sharedDocs',views.sharedDocuments,name="shareddocs"),
    path('addSharedDocs',views.addSharedDocs),
    path('viewSharedDocs',views.viewSharedDocs),
    path('updateSharedDocs',views.updateSharedDocs),
    path('deleteSharedDocs/<int:id>',views.deleteSharedDocs),
    path('assignSharedDocsUser',views.assignSharedDocsUser),

# # path(-------------------Ambika------------------------------),
    path('showDirectors',views.showDirectors,name="showDirectors"),
    path('addMember',views.addMember),
    path('viewMember',views.viewMember),
    path('updateMember',views.updateMember),
    path('deleteMember/<int:id>/<str:name>',views.deleteMember),

    # ==================Voting Resoolution =========
    path('showVotingResolution', views.showVotingResolution),
    path('addVR', views.addVR),
    path('viewVR', views.viewVR),
    path('updateVR', views.updateVR),
    path('deleteVR/<int:id>/<str:filename>', views.deleteVR),
    # path('deleteVR',views.deleteVR),
    path('getUser', views.getUser),
    path('viewassignVR', views.viewassignVR),
    path('assignVR', views.assignVR),
    path('viewActionsVR', views.viewActionsVR),

    # ==================Audit trail =========
    path('showAudit', views.showAudit),
    path('showAuditLogs', views.showAuditLogs),
    path('admin/', admin.site.urls),

    # ++++++++++Encryption+++++++++
    path('Encrypt_Sample',views.Encrypt_Sample),

    # +++++++++++++++++++++++IOS  API Services ++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++Pushpak+++++++++++++++++++++
    path('authenticate_june5_enc', views.authenticate_june5_enc),
    path('MeetingsInfo1_enc', views.MeetingsInfo1_enc),
    path('ret_dashboard', views.ret_dashboard),
    path('add_user_ver_enc', views.add_user_ver_enc),
    path('ret_UserAccess', views.ret_UserAccess),
    path('mpdf_enc', views.mpdf_enc),
    path('agenda_enc', views.agenda_enc),
    path('ret_notes2_new_enc', views.ret_notes2_new_enc),
    path('notes_upload2_new_enc', views.notes_upload2_new_enc),
    path('ret_approvals', views.ret_approvals),
    path('ret_comments', views.ret_comments),

    # ++++++++++++++++++Ambika++++++++++++++
    path('sendPass_enc', views.sendPass_enc),
    path('new_pass_enc', views.new_pass_enc),
    path('action_approval_enc', views.action_approval_enc),
    path('ret_mom_comment', views.ret_mom_comment),
    path('ret_add_comment', views.ret_add_comment),
    path('ret_addBriefcase', views.ret_addBriefcase),
    path('ret_briefcase', views.ret_briefcase),

    # ++++++++++++audittrail log api +++++++
    path('ret_module_details', views.ret_module_details),

    # ++++++++++++++++++++++ vedanti ++++++++++++++
    path('ret_mom_details',views.ret_mom_details),
    path('ret_mom_action',views.ret_mom_action),
    path('ret_sharedDoc',views.ret_sharedDoc),
    path('ret_mail',views.ret_mail),
    path('ret_board',views.ret_board),
    path('archive1_enc',views.archive1_enc),
    path('ret_aboutus_enc',views.ret_aboutus_enc),
    path('calender_enc',views.calender_enc),
    path('ret_module_details',views.ret_module_details),
    path('ret_removeBriefcase',views.ret_removeBriefcase),
    path('Mail',views.Mail),
    path('ret_msg',views.ret_msg),
    path('ret_audittrail',views.ret_audittrail),
    path('ret_snapshot',views.ret_snapshot),

    path('ret_chat', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),


    path('startgroup',views.startgroup),
    path('startPresentation',views.startPresentation),



    # path('signalr',views.signalr),
    # path('signalr/negotiate',views.signalr_negotiate)











]
