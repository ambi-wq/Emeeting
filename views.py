import calendar
import csv
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import traceback
from zipfile import ZipFile
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.platypus import Table, TableStyle
from requests.utils import requote_uri
from .Blowfish_algorithm import encryption, decryption
from .AES_Encryption import encrypt, decrypt
#from captcha.image import ImageCaptcha
import random
import string
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication

from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import ast
import zipfile
import smtplib as s
from django.core.paginator import Paginator
# Create your views here.
from django.template import context
from reportlab.pdfgen import canvas
#from PIL import Image, ImageDraw, ImageFont
from EmeetingApp.models import Committee, Meeting, EmeetCmslogs, EmeetForums, EmeetAnnualMeetings, EmeetMsg
from .models import EmeetApprovals, EmeetApprovalUsers, EmeetBoardMembers
from .API_Encryption import Encryption

object = Encryption()
import traceback
from django.views.decorators.csrf import csrf_exempt
import hashlib
import random as r
import base64
from shutil import copyfile
from .fcm import singleNotification, multipleNotification


#------------------------Local+++++++++++++++++++++++++++++++
baseURL = '/'
basepath = "D:/Workspace/Python Workspace/EmeetingAdmin_Linux_LatestPatch/Emeeting/EmeetingApp/"
resourcesfolderpath = "D:/Workspace/Python Workspace/EmeetingAdmin_Linux_LatestPatch/Emeeting/EmeetingApp/static/resources"

pdfurl = "http://127.0.0.1:8000/static/AboutUs/"
resetpass_link = "http://127.0.0.1:8000/"


#------------------------Linux ++++++++++++++++++++++++++++++++++++++
import os

# # from pathlib import Path
# # home = str(Path.home())
# # print("home----->",home)
# cwd = os.getcwd()
# print("cwd----->", cwd)
# cwd_new = cwd.replace('\\', '/')
# print(cwd_new)
# basepath = cwd_new + "/EmeetingApp/"
# resourcesfolderpath = cwd_new + "/EmeetingApp/static/resources"
# # base11 = 'http://192.168.0.90'
# base11 = 'http://125.99.153.203'
# base12 = base11.replace("http://", "/")
# baseURL = '/'
# # basepath= "D:/project_bk_zips/emeetingadminpythonfiles_V/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/"
# # resourcesfolderpath = "D:/project_bk_zips/emeetingadminpythonfiles_V/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/static/resources"
# pdfurl = base11 + "/static/AboutUs/"
# resetpass_link = base11 + baseURL

#----------------------- Mgenius ++++++++++++++++++++++++++++
# baseURL = '/emeetingadmin/'
# basepath = "C:/HostingSpaces/Mobitrails/mgenius.in/wwwroot/mobitrail/emeetingadminpythonfiles/Emeeting/EmeetingApp/"
# resourcesfolderpath = "C:/HostingSpaces/Mobitrails/mgenius.in/wwwroot/mobitrail/emeetingadminpythonfiles/Emeeting/EmeetingApp/static/resources"
# pdfurl = "https://mgenius.in/emeetingadmin/static/AboutUs/"
# resetpass_link = "https://mgenius.in/emeetingadmin/"

def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


def showcommittee(request):
    if request.session.has_key('session_key'):
        print("Committee Module")
        comitteedata = Committee.objects.all().values()

        final_presentor = []
        qs_json = list(comitteedata)

        fidcollectio = []
        for idcol in qs_json:
            f_id = idcol["fid"]
            fidcollectio.append(f_id)

        for x in fidcollectio:
            cursor = connection.cursor()
            query = "SELECT userid FROM `emeet_manageusers` WHERE FIND_IN_SET(" + str(x) + ", `committee`) > 0"
            cursor.execute(query)
            userid_result = cursor.fetchall()

            arr = []
            for i in userid_result:
                arr.append(i[0])

            presentor = {'Meeting_presentor': arr}
            final_presentor.append(presentor)
        final_comitteedata = []

        for ele, ele1 in zip(qs_json, final_presentor):
            ele.update(ele1)
            final_comitteedata.append(ele)

        query = "SELECT userid FROM `emeet_manageusers` where access = 'user'"
        cursor.execute(query)
        activeuser = cursor.fetchall()
        activeuserarr = []
        for i in activeuser:
            activeuserarr.append(i[0])

        print(activeuserarr)

        # paginator = Paginator(comitteedata, 10)
        # page = request.GET.get('page')
        # comitteedata = paginator.get_page(page)
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        return render(request, "Committee.html",
                      {'comitteedata': final_comitteedata, 'baseURL': baseURL, 'activeuserarr': activeuserarr,
                       'response': response})
    else:
        return redirect(baseURL)


def createcommittee(request):
    if request.session.has_key('session_key'):
        print("Create Committee Module")
        CommitteeName = request.POST.get('CommitteeName')
        print(CommitteeName)
        shortname = request.POST.get('shortName')
        print(shortname)

        path1 = os.path.join(resourcesfolderpath, CommitteeName)
        path = path1.replace('\\', '/')
        print("committee path---->", path)
        os.mkdir(path)
        print("Directory '% s' created" % CommitteeName)

        if CommitteeName != None or shortname != None:
            cursor = connection.cursor()
            stat = "True"
            company_id = "1"
            approved = "approved"
            result_new = cursor.execute("insert into `emeet_forums`(`fname`,`fn`,`stat`,`company_id`,`approved`)"
                                        "values ('" + str(CommitteeName) + "','" + str(shortname) + "','" + str(
                stat) + "','" + str(company_id) + "','" + str(approved) + "')")
            messages.info(request, CommitteeName + ' Created Successfully..!!')
            activityLogs(request, "Created new Commitee" + CommitteeName)
            return redirect(baseURL + 'showcommittee')
        else:
            return redirect(baseURL + 'showcommittee')
    else:
        return redirect(baseURL)


def Assignuser(request):
    if request.session.has_key('session_key'):
        print("Assignuser")
        committeeid = request.POST.get('fid')
        print(committeeid)
        cursor = connection.cursor()
        query = "SELECT userid FROM `emeet_manageusers` WHERE FIND_IN_SET(" + str(committeeid) + ", `committee`) > 0"
        print("query== ",query)
        cursor.execute(query)
        userid_result = cursor.fetchall()
        print("comm result-->",userid_result)
        arr1 = []
        for i in userid_result:
            arr1.append(i[0])

        query = "SELECT userid FROM `emeet_manageusers` where access = 'user'"
        cursor.execute(query)
        activeuser = cursor.fetchall()
        activeuserarr1 = []
        for i in activeuser:
            activeuserarr1.append(i[0])

        jsondata = {"userid": arr1, "Alluser": activeuserarr1, 'fid': committeeid}
        return HttpResponse(json.dumps(jsondata, default=str))
    else:
        return redirect(baseURL)


def downloadCommitteedata(request):
    if request.session.has_key('session_key'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Committee_Master.csv"'
        q = "SELECT @a:=@a+1 Sr, `fname`,`fn`,`stat`,`approved` FROM  emeet_forums , (SELECT @a:= 0) AS a"
        cursor = connection.cursor()
        cursor.execute(q)
        notifications = cursor.fetchall()
        writer = csv.writer(response)
        writer.writerow(['Sr.', 'Committee Name', 'Short Name', 'Status', 'Approve by checker'])
        for data in notifications:
            activity = data[3]
            clean = re.compile('<.*?>')
            result = re.sub(clean, '', activity)
            datalist = list(data)
            datalist.remove(activity)
            datalist.insert(3, result)
            data = tuple(datalist)
            writer.writerow(data)
        # name = "{0}".format(request.session.get('name'))

        activityLogs(request, "Download the Committee data.")
        return response
    else:
        return redirect(baseURL)


def updatecommitteeinfo(request):
    if request.session.has_key('session_key'):
        print("Update Committee information")
        fid = request.POST.get('fid')
        print(fid)
        CommitteeName = request.POST.get('Commitee_Name')
        print(CommitteeName)
        shortname = request.POST.get('shortname')
        print(shortname)
        meeting_presentor = request.POST.get('meeting_presentor')
        print(meeting_presentor)
        status = request.POST.get('status')
        print(status)

        cursor = connection.cursor()
        query = "update emeet_forums set fname='" + CommitteeName + "',fn='" + shortname + "',stat='" + status + "',presentor='" + meeting_presentor + "' where fid ='" + fid + "';"
        cursor.execute(query)
        messages.success(request, 'Committee Information is Successfully Updated.......')

        activityLogs(request, "Update the" + CommitteeName + "Information.")
        return redirect(baseURL + 'showcommittee')
    else:
        return redirect(baseURL)


def updateAssignuser(request):
    if request.session.has_key('session_key'):
        print("Assign User")
        fid = request.POST.get('fid')
        print(fid)
        Assign_user = request.POST.getlist('Assign_user[]')
        print("Assign_user--->",Assign_user)
        cursor = connection.cursor()


        query = "SELECT userid FROM `emeet_manageusers` WHERE FIND_IN_SET(" + str(fid) + ", `committee`) > 0"
        print("query== ", query)
        cursor.execute(query)
        userid_result = cursor.fetchall()

        arr1 = []
        for i in userid_result:
            arr1.append(i[0])
        print("old comm result-->", arr1)
        # for i in Assign_user:
        #     query = "update emeet_manageusers set committee = Concat(committee , ',' ,'" + fid + "') where userid='" + i + "' "
        #     print(query)
        #     cursor.execute(query)

        for ass_u in Assign_user:
            if ass_u in arr1:
                print("ass user-->",ass_u)
                query = "select committee from emeet_manageusers where userid = '"+ass_u+"' "
                cursor.execute(query)
                ass_u_comm = cursor.fetchone()[0]
                print(ass_u_comm)
                if fid in ass_u_comm:
                    print("fid present")
                else:
                    query = "update emeet_manageusers set committee = Concat(committee , ',' ,'" + fid + "') where userid='" + ass_u + "' "
                    print(query)
                    cursor.execute(query)
            else:
                query = "update emeet_manageusers set committee = Concat(committee , ',' ,'" + fid + "') where userid='" + ass_u + "' "
                print("else-->",query)
                cursor.execute(query)

        for old_u in arr1:
            if old_u not in Assign_user:
                query = "select committee from emeet_manageusers where userid = '" + old_u + "' "
                cursor.execute(query)
                oldass_u_comm = cursor.fetchone()[0]
                print(oldass_u_comm)
                oldass_comm_ls = oldass_u_comm.split(',')
                oldass_comm_ls1 = list(filter(lambda a: a != fid, oldass_comm_ls))
                ols_ass_com_str = ','.join(str(x) for x in oldass_comm_ls1)
                print("ols_ass_com_str-->",ols_ass_com_str)
                query = "update emeet_manageusers set committee = '"+ ols_ass_com_str +"' where userid='" + old_u + "' "
                print("else-->", query)
                cursor.execute(query)

        activityLogs(request, "Update the Committee Assign User.")
        return redirect(baseURL + 'showcommittee')
    else:
        return redirect(baseURL)



def manageMeeting(request):
    if request.session.has_key('session_key'):
        print("manageMeeting")
        today_date = datetime.datetime.now()
        cursor = connection.cursor()
        forums = request.POST.get('forums')
        # print(forums)
        selectboxvalue = request.POST.get('selectboxvalue')
        print("selectboxvalue--->", selectboxvalue)
        fidres = ""
        datedisplay = ""
        overdate = []
        current = []
        scheduled = []
        meetingdata = []

        if forums != None:
            query1 = "select fid from emeet_forums where fname = '" + str(forums) + "'"
            cursor.execute(query1)
            res = cursor.fetchone()
            fidres = res[0]

        if selectboxvalue != None or forums != None:
            if "Select" in selectboxvalue:
                meetingdata = Meeting.objects.filter(fid=fidres).order_by('-dt')
                # print("ResultSearch",meetingdata)
            else:
                if "Date" in selectboxvalue:
                    startdate = request.POST.get('startdate')
                    stat_convert = datetime.datetime.strptime(startdate, "%m/%d/%Y").strftime("%Y-%m-%d")
                    enddate = request.POST.get('enddate')
                    end_convert = datetime.datetime.strptime(enddate, "%m/%d/%Y").strftime("%Y-%m-%d")
                    meetingdata = Meeting.objects.filter(fid=fidres, dt__range=(stat_convert, end_convert)).order_by(
                        'dt')
                    # print("ResultSearch1", meetingdata)
                else:
                    if "Meeting_Status" in selectboxvalue:
                        meet_status = request.POST.get('meet_status')
                        print(meet_status)
                        if meet_status != None:
                            print("over")
                            query2 = "select id,dt,days from emeet_meeting where fid='" + str(
                                fidres) + "' and status ='true'"
                            cursor.execute(query2)
                            dateres = cursor.fetchall()
                            # print("-----------",dateres)
                            datearr = []
                            for i in dateres:
                                datedict = {"mid": i[0], "date": i[1], "days": i[2]}
                                datearr.append(datedict)

                            todaydate = datetime.datetime.now()
                            for j in datearr:
                                dt = j["date"]
                                # print(dt)
                                days = j["days"]
                                mid = j["mid"]
                                # print("mid", mid)
                                end_date = dt + datetime.timedelta(days=days)
                                # print("End date", end_date)
                                # for over
                                if "Over" in meet_status:
                                    if todaydate > end_date:
                                        overdict = {"mid": mid}
                                        overdate.append(overdict)
                                elif "Current" in meet_status:
                                    if todaydate < end_date and todaydate > dt:
                                        currentdict = {"mid": mid}
                                        current.append(currentdict)
                                else:
                                    if dt > todaydate:
                                        scheduleddict = {"mid": mid}
                                        scheduled.append(scheduleddict)
                            print("---------------final Result-----------------")
                            print(overdate)
                            print(current)
                            print(scheduled)

                            if "Over" in meet_status:
                                for res in overdate:
                                    print(res)
                                    query3 = "select id,title,dt,status,id from emeet_meeting where id = '" + str(
                                        res["mid"]) + "' and fid = '" + str(fidres) + "' "
                                    cursor.execute(query3)
                                    overres = cursor.fetchall()
                                    for e in overres:
                                        overnewdict = {"mid": "Meetings" + str(e[0]), "title": e[1], "dt": e[2],
                                                       "status": e[3], "id": e[4]}
                                        meetingdata.append(overnewdict)
                            elif "Current" in meet_status:
                                for res1 in current:
                                    # print(res1)
                                    query4 = "select id,title,dt,status,id from emeet_meeting where id = '" + str(
                                        res1["mid"]) + "' and fid = '" + str(fidres) + "' "
                                    cursor.execute(query4)
                                    overres = cursor.fetchall()
                                    for e in overres:
                                        overnewdict1 = {"mid": e[0], "title": e[1], "dt": e[2], "status": e[3],
                                                        "id": e[4]}
                                        meetingdata.append(overnewdict1)
                            else:
                                for res2 in scheduled:
                                    # print(res2)
                                    query5 = "select id,title,dt,status,id from emeet_meeting where id = '" + str(
                                        res2["mid"]) + "' and fid = '" + str(fidres) + "' "
                                    cursor.execute(query5)
                                    overres = cursor.fetchall()
                                    for e in overres:
                                        overnewdict2 = {"mid": "Meetings" + e[0], "title": e[1], "dt": e[2],
                                                        "status": e[3], "id": e[4]}
                                        meetingdata.append(overnewdict2)

        else:
            f = request.GET.get('f')
            if f == None:
                meetingdata = Meeting.objects.all().order_by('-dt')
            else:
                if "Select Committee" in f:
                    meetingdata = Meeting.objects.all().order_by('-dt')
                else:
                    forums = f
                    query1 = "select fid from emeet_forums where fname = '" + str(forums) + "'"
                    cursor.execute(query1)
                    res = cursor.fetchone()
                    fidres1 = res[0]
                    meetingdata = Meeting.objects.filter(fid=fidres1).order_by('-dt')

        query = "select fid,fname from emeet_forums where stat = 'true' or stat = 'True'"
        cursor.execute(query)
        committee_info = cursor.fetchall()

        committee_array = []
        for i in committee_info:
            fid_dict = {"fid": i[0]}
            fname_dict = {"fname": i[1]}
            fid_dict.update(fname_dict)
            committee_array.append(fid_dict)

        # print(meetingdata)

        if forums == None:
            forums = "Select Committee"

        if selectboxvalue != None:
            if "Date" in selectboxvalue or "Meeting_Status" in selectboxvalue:
                datedisplay = "hide"

        range1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

        range2 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

        for i in range(11, 60):
            range2.append(i)

        query10 = "select id,dt,days from emeet_meeting"
        cursor.execute(query10)
        expirydate = cursor.fetchall()
        print("-------------")
        # print(expirydate)

        Expirydatearray = []
        for expdate in expirydate:
            days = expdate[2]
            end_date = expdate[1] + datetime.timedelta(days=days)
            expdatedict = {"id": expdate[0], "ExpiryDate": end_date}
            Expirydatearray.append(expdatedict)

        # print(Expirydatearray)

        query14 = "select fid,mid from emeet_meeting"
        cursor.execute(query14)
        allfid = cursor.fetchall()
        print("=============================",allfid)

        fidmidarr = []
        for id in allfid:
            fid = id[0]
            mid = id[1]

            iddict = {"fid": fid, "mid": mid}
            fidmidarr.append(iddict)

        print("fidmidarr--------------------->",fidmidarr)
        mom_id_arr = []
        for e in fidmidarr:
            print(e)
            e_fid = e["fid"]
            e_mid = e["mid"]

            q = "select id from emeet_mom1 where fid = '" + str(e_fid) + "' and mid = '" + str(e_mid) + "'"
            cursor.execute(q)
            mom_id = cursor.fetchall()
            #print(mom_id)

            mom_multi_arr = []
            if len(mom_id) > 0:
                for w in mom_id:
                    mom_id_multi = w[0]
                    mom_multi_arr.append(mom_id_multi)

                iddict1 = {"fid": e_fid, "mid": e_mid, "momid": mom_multi_arr}
                mom_id_arr.append(iddict1)
            else:
                pass

        print("mom_id_arr---------------->",mom_id_arr)

        commentcount = []
        for g in mom_id_arr:
            g_fid = g["fid"]
            g_mid = g["mid"]
            mom_id_new = g["momid"]

            m = mom_id_new[len(mom_id_new) - 1]
            query20 = "select count(comment) from emeet_mom_comment where momid = '" + str(m) + "'"
            cursor.execute(query20)
            res4 = cursor.fetchone()
            if len(res4) > 0:
                # print(res4)
                commentcountdict = {"fid": g_fid, "mid": g_mid, "count": res4[0], "momid": m}
                commentcount.append(commentcountdict)
            # for m in mom_id_new:
            #     query20 = "select count(comment) from emeet_mom_comment where momid = '" + str(m) + "'"
            #     cursor.execute(query20)
            #     res4 = cursor.fetchone()
            #     if len(res4) > 0:
            #         # print(res4)
            #         commentcountdict = {"fid": g_fid, "mid": g_mid, "count": res4[0], "momid": m}
            #         commentcount.append(commentcountdict)

        print("-----------------==========")
        print("commentcount--------------------------->",commentcount)

        final_count_comment = []
        for m in commentcount:
            count = m["count"]
            if count > 0:
                momid = m["momid"]
                countquery = "select approve_status from emeet_mapping_agenda where mom_id = '" + str(momid) + "'"
                cursor.execute(countquery)
                approvestat = cursor.fetchall()
                # print(approvestat)

                approvestatarr = []
                if len(approvestat) > 0:
                    for stat in approvestat:
                        approvestatarr.append(stat[0])

                # print(approvestatarr)

                if len(approvestatarr) > 0:
                    statusres1 = most_frequent(approvestatarr)
                    # print(statusres1)

                    if "Rejected" in statusres1:
                        pass
                    else:
                        stat_fid = m["fid"]
                        stat_mid = m["mid"]

                        finalcountdict = {"fid": stat_fid, "mid": stat_mid, "count": count, "momid": momid}
                        final_count_comment.append(finalcountdict)
            else:
                finalcountdict = {"fid": m['fid'], "mid": m['mid'], "count": m['count'], "momid": m['momid']}
                final_count_comment.append(finalcountdict)

        print('arr-->', final_count_comment)

        max_comment_count = []
        comment1id = []
        if len(final_count_comment) > 0:
            for n in final_count_comment:
                n_fid = str(n["fid"])
                n_mid = str(n["mid"])
                comment1id.append(n_mid)
                n_mom_id = n["momid"]
                # print("fid-->",n_fid,n_mid,type(n_mid))
                query22 = "select id from emeet_meeting where fid='" + n_fid + "' and mid='" + n_mid + "' "

                cursor.execute(query22)
                max_final_comment = cursor.fetchall()
                print("final comm-->", max_final_comment)
                if len(max_final_comment) > 0:
                    max_final_comment = max_final_comment[0][0]
                else:
                    max_final_comment = 0

                max_comment_count_dict = {"id": max_final_comment, "count": n["count"], "momid": n_mom_id}
                max_comment_count.append(max_comment_count_dict)
                print("max_comment_count_dict ------------>",max_comment_count_dict)

        querycomment = "Select id from emeet_meeting"
        cursor.execute(querycomment)
        comment_0_id = cursor.fetchall()
        print("comment_0_id---------------->",comment_0_id)

        for id_1 in comment_0_id:
            id0 = id_1[0]
            #print("id0---------------->",id0)
            print("comment1id------------>",comment1id)
            if str(id0) not in comment1id:
                max_comment_count_dict1 = {"id": id0, "count": "0", "momid": "0"}
                max_comment_count.append(max_comment_count_dict1)

        print("--------------------------------------")
        print("max comm count--->", max_comment_count)

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        # print("pg meeting====>\n",meetingdata)

        datalength = len(meetingdata)
        paginator = Paginator(meetingdata, 10)
        page = request.GET.get('page')
        meetingdata = paginator.get_page(page)

        return render(request, "meeting.html",
                      {'meetingdata': meetingdata, 'baseURL': baseURL, 'committee_array': committee_array,
                       'forums': forums, 'datedisplay': datedisplay, 'range1': range1, 'rangemin': range2,
                       'today_date': today_date,
                       "Expirydatearray": Expirydatearray, "max_comment_count": max_comment_count, 'response': response,
                       'datalength': datalength})
    else:
        return redirect(baseURL)


def convert24(str1):
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

        # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

        # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:8]


def AddNewMeeting(request):
    if request.session.has_key('session_key'):
        print("Create New Meeting")
        cursor = connection.cursor()
        meet_type = request.POST.get('meet_type')
        title = request.POST.get('title')
        forums = request.POST.get('forums')
        venue = request.POST.get('venue')
        Select_Date1 = request.POST.get('Select_Date')
        print("add meet date--->", Select_Date1)
        Select_Date = datetime.datetime.strptime(Select_Date1, "%d/%m/%Y").strftime("%Y-%m-%d")
        print("date", Select_Date)

        hour = request.POST.get('hour')
        print("Hour", hour)
        min = request.POST.get('min')
        print("min", min)
        timestatus = request.POST.get('timestatus')
        print("timestatus", timestatus)
        totaldays = request.POST.get('totaldays')

        x = hour + ":" + min + ":00 " + timestatus
        resultdate = convert24(x)
        print(resultdate)

        combine = Select_Date + " " + resultdate
        print(combine)

        query7 = "select fid from emeet_forums where fname = '" + str(forums) + "'"
        cursor.execute(query7)
        fidresult = cursor.fetchone()
        fid = fidresult[0]
        print(fid)

        query8 = "select max(mid) from emeet_meeting where fid = '" + str(fid) + "'"
        cursor.execute(query8)
        midresult = cursor.fetchone()
        print("----------------", midresult)
        if midresult[0] != None:
            mid = int(midresult[0]) + 1
            print(mid)
        else:
            mid = "1"

        # query222 = "select max(id) from emeet_meeting"
        # cursor.execute(query222)
        # maxid = cursor.fetchone()
        # id = int(maxid[0]) + 1

        status = "true"
        query11 = "insert into `emeet_meeting`(`mid`,`dt`,`fid`,`status`,`title`,`venue`,`days`) values ('" + str(
            mid) + "','" + str(combine) + "','" + str(fid) + "','" + str(status) + "','" + str(title) + "','" + str(
            venue) + "','" + str(totaldays) + "')"

        cursor = connection.cursor()
        res3 = cursor.execute(query11)

        Meetingquery = "select id from emeet_meeting where title='" + str(title) + "'"
        cursor.execute(Meetingquery)
        Meetingid1 = cursor.fetchone()
        Meetingid = Meetingid1[0]

        path = os.path.join(resourcesfolderpath + "/" + str(forums), str(Meetingid))
        os.mkdir(path)
        print("Directory '% s' created" % Meetingid)

        activityLogs(request, "Added Meeting for " + str(forums) + " AS " + str(title))
        if meet_type == 'add-meeting':
            return redirect(baseURL + "manageMeeting")

        elif meet_type == 'add-agenda':
            print("add agenda ")
            # Meetingid = 12
            url = baseURL + "info/" + str(Meetingid)
            print("url====  ", url)
            return HttpResponse(url)
    else:
        return redirect(baseURL)


def Removemeeting(request):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()
        removeuserlist = request.POST.getlist('Removemeeting[]')
        print(removeuserlist)

        # for j in removeuserlist:
        #     Meetingid = j
        #     removequery = "Select fid from emeet_meeting where id ='"+str(j)+"'"
        #     cursor.execute(removequery)
        #     getfname = cursor.fetchone()
        #     getfid = getfname[0]
        #
        #     GetCommittee = "Select fname from emeet_forums where fid='" + str(getfid) + "'"
        #     cursor.execute(GetCommittee)
        #     committename = cursor.fetchone()
        #     forums = committename[0]

        for i in removeuserlist:
            cursor.execute("Delete from emeet_meeting where id ='" + str(i) + "'")

        #     path = os.path.join(resourcesfolderpath + "/" + str(forums), str(Meetingid))
        #     shutil.rmtree(path)
        #     print("% s removed successfully" % path)
        #
        # activityLogs(request, "Meeting Deleted of"+ forums)

        return redirect(baseURL + "manageMeeting")
    else:
        return redirect(baseURL)


def downloadAllMeetingdata(request):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Meeting_Master.csv"'

        q = "SELECT @a:=@a+1 Sr,`title`,`fid`,`dt`,`status` FROM emeet_meeting ,(SELECT @a:= 0) AS a ORDER BY dt DESC"
        cursor.execute(q)
        meetingdata = cursor.fetchall()

        print(meetingdata)

        temptuple = []
        for m in meetingdata:
            #q = "SELECT fname from emeet_forums where fid ='" + str(m[2]) + "'"
            q = "SELECT fname from emeet_forums where fid ='" + str(m[2]) + "' and  stat = 'true'"
            cursor.execute(q)
            fnameres = cursor.fetchone()

            if fnameres:
                fname = fnameres[0]
                m = list(m)
                m.pop(2)
                m.insert(2, fname)
                m = tuple(m)
                temptuple.append(m)
        print(temptuple)

        writer = csv.writer(response)
        writer.writerow(['Sr.', 'Title', 'Committee Name', 'Date', 'Status'])

        for meeting in temptuple:
            writer.writerow(meeting)

        activityLogs(request, "Download meeting information for All committee.")
        return response
    else:
        return redirect(baseURL)


def Changepublishstatus(request):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()
        uniqueid = request.POST.get('uniqueid')
        print(uniqueid)
        status = request.POST.get('status')
        print(status)
        meetingname = ""

        query212 = "select title,fid from emeet_meeting where id ='" + str(uniqueid) + "'"
        cursor.execute(query212)
        meetingname1 = cursor.fetchall()

        print("meetingname1------------>", meetingname1)
        fid = ""
        for m in meetingname1:
            meetingname = m[0]
            fid = m[1]
        print("fid------------>", fid)
        query213 = "select fname from emeet_forums where fid = '" + str(fid) + "'"
        cursor.execute(query213)
        committe_name = cursor.fetchone()
        print("commit name------------>", committe_name)
        cname = committe_name[0]

        if status == "true":
            newstatus = "false"
            query12 = "update emeet_meeting set status ='" + str(newstatus) + "' where id = '" + str(uniqueid) + "'"
            cursor.execute(query12)
        else:
            newstatus1 = "true"
            query13 = "update emeet_meeting set status ='" + str(newstatus1) + "' where id = '" + str(uniqueid) + "'"
            cursor.execute(query13)

        activityLogs(request, "Publish or Hide:" + meetingname + "for" + cname)
        return redirect(baseURL + "manageMeeting")
    else:
        return redirect(baseURL)


def downloadforumsbasedata(request):
    if request.session.has_key('session_key'):
        f = request.GET.get('f')
        print(f)
        cursor = connection.cursor()
        query1 = "select fid from emeet_forums where fname = '" + str(f) + "'"
        cursor.execute(query1)
        res = cursor.fetchone()
        fidres = res[0]

        meetingdata = Meeting.objects.filter(fid=fidres).order_by('-dt')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + f + 'Meeting_Master.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Committee Name', 'Date', 'Status'])

        for meeting in meetingdata:
            x = [meeting.title, f, meeting.dt, meeting.status]
            writer.writerow(x)

        activityLogs(request, "Download the" + f + "Information.")
        return response
    else:
        return redirect(baseURL)


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


def DraftMOMsite(request):
    if request.session.has_key('session_key'):
        print("DraftMOMsite")
        mid = request.GET.get('mid')
        mid = mid.replace(" ", "")
        print("mid", mid)

        fid = request.GET.get('f_id')
        print("fid--------->", fid)

        cursor = connection.cursor()
        draftquery = "select title from emeet_meeting where id ='" + str(mid) + "' and fid ='" + str(fid) + "'"
        cursor.execute(draftquery)
        draft_res = cursor.fetchone()
        print(draft_res)
        meeting_title = draft_res[0]

        draftquery1 = "SELECT max(title) FROM `emeet_mom1` WHERE fid = '" + str(fid) + "' and mid = '" + str(mid) + "'"
        cursor.execute(draftquery1)
        draft_res1 = cursor.fetchone()
        print(draft_res1)
        draft_title = draft_res1[0]
        print(draft_title)

        if draft_title != None:
            e = draft_title.split()
            data = e[2]
            ds = list(data)
            version_no = int(ds[1]) + 1
            newversion = "v" + str(version_no)
            print(newversion)
            remove = e.pop(2)
            res = e.insert(2, newversion)
            final_res = listToString(e)
            print(final_res)
        else:
            final_res = "Draft MOM v1"

        range1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

        range2 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

        for i in range(11, 60):
            range2.append(i)

        draftquery2 = "SELECT ename FROM `emeet_manageusers` WHERE FIND_IN_SET(" + str(fid) + ", `committee`) > 0"
        cursor.execute(draftquery2)
        draft_res2 = cursor.fetchall()
        print(draft_res2)

        userarr = []
        for e in draft_res2:
            ename = e[0]
            userarr.append(ename)

        print("userarr--------------------------->", userarr)

        draftquery3 = "Select id,title,expirydate from emeet_mom1 where fid = '" + str(fid) + "' and mid = '" + str(
            mid) + "' "
        cursor.execute(draftquery3)
        momres = cursor.fetchall()
        print(momres)

        draftmom = []
        momidarr = []
        if momres != None or len(momres) > 0:
            for mom in momres:
                momid = mom[0]
                momidarr.append(momid)
                draft_title = mom[1]
                expirydate = mom[2]
                momdict = {"draft_title": draft_title, "expirydate": expirydate, "momid": momid}
                draftmom.append(momdict)
            print(draftmom)
        else:
            draftmomlength = 0

        statusdictres = []
        for mom_id in momidarr:
            approve_status_arr = []
            draftquery4 = "Select approve_status from emeet_mapping_agenda where mom_id ='" + str(mom_id) + "'"
            cursor.execute(draftquery4)
            approve_status_res = cursor.fetchall()
            if approve_status_res != None or len(approve_status_res) > 0:
                for status in approve_status_res:
                    approve_status_arr.append(status[0])

            statusdict = {"momid": mom_id, "res": approve_status_arr}
            statusdictres.append(statusdict)

        print("--------", statusdictres)

        finalstatusres = []
        for j in statusdictres:
            mom_id = j["momid"]
            statusres = j["res"]

            if len(statusres) > 1:
                statusresult = most_frequent(statusres)
            elif len(statusres) == 1:
                statusresult = statusres[0]

            final_status_dict = {"momid": mom_id, "status": statusresult}
            finalstatusres.append(final_status_dict)

        print(finalstatusres)

        draftquery5 = "Select id from emeet_mom1 where fid = '" + str(fid) + "' and mid = '" + str(mid) + "' "
        cursor.execute(draftquery5)
        momidres = cursor.fetchall()
        print("---------------", momidres)

        finalcommentcountarr = []
        for _id in momidres:
            momid = _id[0]
            draftquery6 = "Select count(comment) from emeet_mom_comment where momid = '" + str(momid) + "'"
            cursor.execute(draftquery6)
            commentcount = cursor.fetchone()
            comment_res = commentcount[0]
            comment_dict = {"momid": momid, "commentcount": comment_res}
            finalcommentcountarr.append(comment_dict)

        print("+++++++++++++++", finalcommentcountarr)

        draftquery22 = "select max(title) from emeet_mom1 where mid = '" + str(mid) + "' and fid = '" + str(fid) + "'"
        cursor.execute(draftquery22)
        enabledres = cursor.fetchone()
        drafttitleenabled = enabledres[0]
        print(drafttitleenabled)

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        return render(request, "DraftMom.html",
                      {"meeting_title": meeting_title, "Drafttitle": final_res, "range1": range1,
                       "rangemin": range2, "Users": userarr, "momdict": draftmom, "Approved_status": finalstatusres,
                       "baseURL": baseURL, "finalcommentcountarr": finalcommentcountarr,
                       "drafttitleenabled": drafttitleenabled, 'response': response, 'mid': mid, 'fid': fid})
    else:
        return redirect(baseURL)


def Draftuserstatus(request, id):
    if request.session.has_key('session_key'):
        print(id)

        cursor = connection.cursor()
        userstatusquery = "Select userid,approve_status,comments from emeet_mapping_agenda where mom_id ='" + str(
            id) + "'"
        cursor.execute(userstatusquery)
        userstat = cursor.fetchall()

        userstatusdata = []
        for userstatus in userstat:
            print(userstatus)
            userid = userstatus[0]
            status = userstatus[1]
            comments = userstatus[2]

            statusdict = {"userid": userid, "status": status, "comments": comments}
            userstatusdata.append(statusdict)

        print(userstatusdata)
        activityLogs(request, "User viewed Approval status for MOM ID-" + str(id))

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        return render(request, "DraftMom.html",
                      {"userstatusdata": userstatusdata, "userstatusflag": "True", "baseURL": baseURL,
                       'response': response})
    else:
        return redirect(baseURL)


def Draftusercomment(request, id):
    if request.session.has_key('session_key'):
        print(id)

        cursor = connection.cursor()
        usercommentquery = "Select title,comment,senderid,dt,pageno from emeet_mom_comment where momid = '" + str(
            id) + "'"
        cursor.execute(usercommentquery)
        usercomments = cursor.fetchall()
        print(usercomments)

        finalusercomments = []
        for res in usercomments:
            draft_title = res[0]
            userid = res[2]
            dt = res[3]
            page_no = res[4]

            comments = res[1]
            print(comments)

            # comments = comments.encode('utf-8')
            # print(decryption(comments))

            commentsdict = {"title": draft_title, "dt": dt, "page_no": page_no, "userid": userid, "comments": comments}
            finalusercomments.append(commentsdict)

        print("finalusercomments", finalusercomments)

        activityLogs(request, "User viewed MOM comments for MOM ID-" + str(id))

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        return render(request, "DraftMom.html",
                      {"finalusercomments": finalusercomments, "userstatusflag": "False", "baseURL": baseURL,
                       'response': response})
    else:
        return redirect(baseURL)


def EditDraft(request):
    if request.session.has_key('session_key'):
        print("++++++++++++++++++++++EditDraft Called() +++++++++++++++++++++++++++++++++++++")
        momid = request.POST.get('momid')
        print("momid------------", momid)

        cursor = connection.cursor()
        editdraftquery = "select expirydate from emeet_mom1 where id = '" + str(momid) + "'"
        cursor.execute(editdraftquery)
        expirydate = cursor.fetchone()
        enddate = expirydate[0]
        print(enddate)

        onlydate = enddate.date()
        print("onlydate", onlydate)

        onlytime = enddate.time()
        # print("onlytime",onlytime)

        expirytime = datetime.datetime.strptime(str(onlytime), "%H:%M:%S")
        expirytimeresult = expirytime.strftime("%I:%M %p")
        print("onlytime", expirytimeresult)

        fianl_time = expirytimeresult.split()
        print(fianl_time)

        dtime = fianl_time[0]
        AMPMdata = fianl_time[1]

        timeres = dtime.split(":")
        print(timeres)
        time_hour = timeres[0]
        time_min = timeres[1]

        print("timehour", time_hour)
        print("time_min", time_min)
        print("AMPMdata", AMPMdata)

        assignuser = "select userid from emeet_mapping_agenda where mom_id = '" + str(momid) + "'"
        cursor.execute(assignuser)
        assignuser1 = cursor.fetchall()
        totaluserid = []
        for i in assignuser1:
            totaluserid.append(i[0])

        print("totaluserid----------->",totaluserid)
        Assignuserlist = []
        for uname in totaluserid:
            userquery = "select ename from emeet_manageusers where userid = '" + str(uname) + "'"
            cursor.execute(userquery)
            s = cursor.fetchone()
            ename = s[0]
            Assignuserlist.append(ename)

        print("Assignuserlist---------------->",Assignuserlist)

        jsondata = {"Assignuserlist": Assignuserlist, "Expirydate": onlydate, "Expirytime": expirytimeresult,
                    "time_hour": time_hour, "time_min": time_min, "AMPMdata": AMPMdata, "momid": momid}

        activityLogs(request, "User have Edit the Information for MOM-id:" + str(momid))
        return HttpResponse(json.dumps(jsondata, default=str))
    else:
        return redirect(baseURL)


def UpdateDraftMOM(request):
    if request.session.has_key('session_key'):
        print("------------------Update Draft MOM------------------")
        momiduser1 = ""
        momid = request.POST.get('momid')
        Assign_user = request.POST.getlist('selected2[]')
        mailbox = request.POST.get('mailbox')
        mid = request.POST.get('mid')
        fid = request.POST.get('fid')
        Expirydate = request.POST.get('expirydate')
        hour = request.POST.get('hour')
        min = request.POST.get('min')
        timestatus = request.POST.get('AMPM')

        print("momid------------>",momid)
        print("Assign_user--------------------->",Assign_user)
        x = hour + ":" + min + ":00 " + timestatus
        resultdate = convert24(x)
        # print(resultdate)

        combine = Expirydate + " " + resultdate
        print(combine)

        print(momid, mailbox, Assign_user, mid, fid, Expirydate)
        cursor = connection.cursor()

        email_list = []

        for user in Assign_user:
            getemailid = "Select email from emeet_manageusers where ename = '" + str(user) + "'"
            cursor.execute(getemailid)
            emailidres = cursor.fetchone()
            email_list.append(emailidres[0])

        print('email_list------> ', email_list)

        query = "select emeet_forums.fname,emeet_meeting.dt from `emeet_meeting` INNER JOIN emeet_forums " \
                "where emeet_meeting.id= '" + mid + "' and emeet_forums.fid = '" + fid + "' and emeet_forums.fid = emeet_meeting.fid"
        cursor.execute(query)
        emaildata = cursor.fetchall()[0]
        forum_name = emaildata[0]
        dbdatetime = (emaildata[1])
        date_time = dbdatetime.strftime('%Y-%m-%d|%I:%M %p')
        day_name = dbdatetime.strftime("%A")
        date = date_time.split('|')[0]
        time = date_time.split('|')[1]

        print("emaildata------>> ", emaildata, "\n", forum_name, date, time, day_name)

        if mailbox == 'true':
            print("in email")
            sendDraftMomMail(email_list, forum_name, date, time, Expirydate, day_name)

        momiduserarr = []
        updatequery1 = "Select userid from emeet_mapping_agenda where mom_id = '" + str(momid) + "'"
        cursor.execute(updatequery1)
        momiduser = cursor.fetchall()
        print(momiduser)

        if len(momiduser) > 0:
            for j in momiduser:
                momiduserarr.append(j[0])

            print(momiduserarr)

        Assign_user_arr = []
        for i in Assign_user:
            updatequery2 = "Select userid from emeet_manageusers where ename = '" + str(i) + "'"
            cursor.execute(updatequery2)
            momiduser1 = cursor.fetchall()
            print(momiduser1)
            userinlist = momiduser1[0][0]
            Assign_user_arr.append(userinlist)

        print("Assign_user_arr---------------------->",Assign_user_arr)

        for h in Assign_user_arr:
            existuser = "Select count(*) from emeet_mapping_agenda where userid = '" + str(
                h) + "' and mom_id = '" + str(momid) + "'"
            cursor.execute(existuser)
            res = cursor.fetchone()
            print("res------------>",res,"| res[0]==>",res[0])
            if res[0] == None or res[0] == 0:

                approve_status = "Pending"
                insertdate = datetime.datetime.now()

                insertnewuser = "insert into `emeet_mapping_agenda`(`mom_id`,`userid`,`approve_status`,`InsertDateTime`) values ('" + str(
                    momid) + "','" + str(h) + "','" + str(approve_status) + "','" + str(insertdate) + "')"
                cursor.execute(insertnewuser)
                print("inserted !!")
            else:
                pass

        deletedarr = []
        for k in momiduserarr:
            if k not in Assign_user_arr:
                deletedarr.append(k)
            else:
                pass

        print(deletedarr)

        if len(deletedarr) > 0:
            for removeuser in deletedarr:
                removeuserinlist = "Delete from emeet_mapping_agenda where userid ='" + str(
                    removeuser) + "' and mom_id = '" + str(momid) + "'"
                cursor.execute(removeuserinlist)

        jsondata1 = {"status": "success"}

        activityLogs(request, "User have Update the Draft MOM Information for MOM-id:" + str(momid))
        return HttpResponse(json.dumps(jsondata1, default=str))
    else:
        return redirect(baseURL)


def Momcomments(request, id):
    if request.session.has_key('session_key'):
        print(id)

        if id != 0:
            cursor = connection.cursor()
            mom_query = "select title,comment,senderid,dt,pageno from emeet_mom_comment where momid = '" + str(id) + "'"
            cursor.execute(mom_query)
            momres = cursor.fetchall()

            momcomment_arr = []
            if len(momres) > 0:
                for i in momres:
                    print(i)
                    mom_comment_dict = {"title": i[0], "comments": i[1], "userid": i[2], "dt": i[3], "page_no": i[4]}
                    momcomment_arr.append(mom_comment_dict)

            name = "{0}".format(request.session.get('ename'))
            date_time = "{0}".format(request.session.get('date_time'))
            response = name + " " + date_time

            activityLogs(request, "User viewed MOM comments for MOM ID-" + str(id))
            return render(request, "meeting.html",
                          {"momcomment_arr": momcomment_arr, "momcomment_arr1": "True", "baseURL": baseURL,
                           'response': response})
        else:
            activityLogs(request, "User viewed MOM comments for MOM ID-" + str(id))
            momcomment_arr = []

            name = "{0}".format(request.session.get('ename'))
            date_time = "{0}".format(request.session.get('date_time'))
            response = name + " " + date_time

            return render(request, "meeting.html",
                          {"momcomment_arr": momcomment_arr, "momcomment_arr1": "True", "baseURL": baseURL,
                           'response': response})
    else:
        return redirect(baseURL)


def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundereds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundereds +
           tens + ones)

    return ans.lower();


def getalphaID(i):
    alphabets = ["0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                 "t", "u", "v", "w", "x", "y", "z", "aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh", "ii", "jj", "kk",
                 "ll", "mm", "nn", "oo", "pp", "qq", "rr", "ss", "tt", "uu", "vv", "ww", "xx", "yy", "zz"];
    return alphabets[i]


def DownloadReports(request, id):
    if request.session.has_key('session_key'):
        # print(id)
        cursor = connection.cursor()

        query = "SELECT * FROM `emeet_meeting` where id  ='" + str(id) + "'"
        cursor.execute(query)
        meeting_info = cursor.fetchall()

        title = ''
        venue = ''
        vdate = ''
        print(meeting_info)
        for i in meeting_info:
            vdate = i[1].strftime('%B %Y')
            time = i[1].strftime('%H:%M %p')
            day = i[1].strftime('%d')
            if int(day) < 10:
                day = "0" + day
            venue = i[6]
            title = i[5]

        agenda_response = []

        query = "SELECT ag_id,title,doc,mid,version,aid FROM `emeet_level0` where mid  ='" + str(id) + "' order by aid"
        cursor.execute(query)
        level0 = cursor.fetchall()
        print(level0)
        agendalen = len(level0)
        agendalen = len(level0)
        if agendalen > 0:
            agenda_ag_id = []
            for li in level0:
                agenda_ag_id.append(li[0])
            print("agenda_ag_id--->", agenda_ag_id)
            query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level1` where parent in (" + str(
                agenda_ag_id).strip('[]') + ") order by aid"
            print("query1---->", query)
            cursor.execute(query)
            level1 = cursor.fetchall()
            print(level1)
            subagendalen = len(level1)

            subagenda_ag_id = []
            if subagendalen > 0:
                for li in level1:
                    subagenda_ag_id.append(li[0])

                query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level2` where parent in (" + str(
                    subagenda_ag_id).strip('[]') + ") order by aid"
                cursor.execute(query)
                level2 = cursor.fetchall()
                print(level2)
                subsubagendalen = len(level2)
                print(level0)
                print(level1)
                print(level2)
                subsubagenda_ag_id = []
                for li in level2:
                    subsubagenda_ag_id.append(li[0])

            for ag in level0:
                subagendaarr = []

                sss = {}
                ag_title = str(ag[5]) + "." + str(ag[1])
                ag_doc = str(ag[2])

                agenda = {"ag_title": ag_title, "ag_doc": ag_doc, "ag_id": ag[0], "aid": ag[5]}
                sss["agenda"] = agenda

                for sag in level1:
                    if sag[2] == ag[0]:
                        subsubarr = []

                        tmp = getalphaID(sag[5])
                        sag_title = str(ag[5]) + ".(" + tmp + ")" + str(sag[1])
                        sag_doc = str(sag[3])
                        sub_agenda = {"sag_title": sag_title, "sag_doc": sag_doc, "sag_id": sag[0], "said": sag[5]}

                        subagendaarr.append(sub_agenda)
                        sss["sub_agenda"] = subagendaarr
                        for ssag in level2:
                            if ssag[2] == sag[0]:
                                tmp1 = intToRoman(ssag[5])
                                ssag_title = str(ag[5]) + ".(" + tmp + ")" + "(" + tmp1 + ")" + str(ssag[1])
                                ssag_doc = str(ssag[3])
                                subsubagenda = {"ssag_title": ssag_title, "ssag_doc": ssag_doc, "ssag_id": ssag[0],
                                                "said": ssag[5]}

                                subsubarr.append(subsubagenda)
                                sub_agenda['subsubagenda'] = subsubarr

                agenda_response.append(sss)

        print(agenda_response)
        print("agenda =====>", agenda_response)

        reportquery = "Select fid,title from emeet_meeting where id ='" + str(id) + "'"
        cursor.execute(reportquery)
        result_1 = cursor.fetchall()
        print(result_1)

        d = []
        for r in result_1:
            fid = r[0]
            d.append(fid)
            title = r[1]
            d.append(title)

        csvtitle = d[1]
        reportquery7 = "select fname from emeet_forums where fid = '" + str(d[0]) + "'"
        cursor.execute(reportquery7)
        committee_name = cursor.fetchone()
        fname = committee_name[0]

        filename = fname + "-" + csvtitle

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
        writer = csv.writer(response)

        for data in agenda_response:
            print("data===>   ", data)
            # agenda_data\
            writer.writerow([])
            for key, value in data.items():
                if key == 'agenda':
                    agtitle = value['ag_title']
                    print(agtitle)
                    writer.writerow([agtitle])

                elif key == 'sub_agenda':
                    for sag in value:
                        sagtitle = sag['sag_title']
                        print(sagtitle)
                        writer.writerow(['', sagtitle])

                        if 'subsubagenda' in sag.keys():
                            for ssag in sag['subsubagenda']:
                                ssagtitle = ssag['ssag_title']
                                print(ssagtitle)
                                writer.writerow(['', '', ssagtitle])
                        else:
                            continue

        # activityLogs(request, "User" + str(id))

        return response
    else:
        return redirect(baseURL)


def split(word):
    return list(word)


def sendDraftMomMail(email, forum_name, date, time, Expirydate, day_name):
    print("======================= draft mom mail ================")
    print(email, forum_name, date, time, Expirydate, day_name)

    cursor = connection.cursor()
    cursor.execute("select * from `emeet_mailformat` where `type` = 'MomUpload' ")
    email_query = cursor.fetchall()
    email_format = email_query[0]
    subject = email_format[1]
    body = email_format[2]

    email_id = "vedanti@mobitrail.com"

    try:

        ob = s.SMTP("smtp.gmail.com", 587)
        ob.starttls()
        ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
        msg = MIMEMultipart('alternative')
        msg['From'] = 'mobitrail.technology@gmail.com'
        msg['To'] = email_id
        msg['Subject'] = subject

        body = body.replace("[ForumName]", forum_name)
        body = body.replace("[AMPMTime]", time)
        body = body.replace("[DayTime]", day_name)
        body = body.replace("[DateTime]", date)
        body = body.replace("[ExpiryDateString]", Expirydate)

        html = body

        part1 = MIMEText(html, 'html')
        # part2 = MIMEText("Dear " + name + ", \n\n" \
        #                                   "Please click on the below link to reset your password. \n\n" \
        #                                   "Click Here to Reset \n\n" \
        #                                   "Regards,\n\n" \
        #                                   "Secretarial Team.", 'text')

        # reciever = "vedanti@mobitrail.com" #email of person
        msg.attach(part1)
        # msg.attach(part2)
        # print(msg.as_string())

        ob.sendmail('mobitrail.technology@gmail.com', email_id, msg.as_string())
        print("successsful")
        ob.quit()

    except Exception as e:
        print("Err: ", e)


def NewDraftMOM(request):
    if request.session.has_key('session_key'):
        print("------------- NewDraftMOM -----------------")
        file_data = request.FILES.get('file')
        data = request.POST.get('requestData')
        request_data = json.loads(data)
        print("------>>", request_data)

        meeting_title = request_data["meeting_title"]
        Drafttitle = request_data["title"]
        Expirydate = request_data["expirydate"]
        hour = request_data["hour"]
        min = request_data["min"]
        timestatus = request_data["AMPM"]
        sendmail = request_data["sendmail"]
        selectuser = request_data["selecteuser"]
        mid = request_data["mid"]
        fid = request_data["fid"]
        print("req data fid--->",fid)


        x = hour + ":" + min + ":00 " + timestatus
        resultdate = convert24(x)
        # print(resultdate)

        combine = Expirydate + " " + resultdate
        print(combine)

        email_list = []
        cursor = connection.cursor()
        for user in selectuser:
            getemailid = "Select email from emeet_manageusers where ename = '" + str(user) + "'"
            cursor.execute(getemailid)
            emailidres = cursor.fetchone()
            email_list.append(emailidres[0])

        print('email_list------> ', email_list)

        query = "select emeet_forums.fname,emeet_meeting.dt from `emeet_meeting` INNER JOIN emeet_forums " \
                "where emeet_meeting.id= '" + mid + "' and emeet_forums.fid = '" + fid + "' and emeet_forums.fid = emeet_meeting.fid"
        cursor.execute(query)
        emaildata = cursor.fetchall()[0]
        forum_name = emaildata[0]
        dbdatetime = (emaildata[1])
        date_time = dbdatetime.strftime('%Y-%m-%d|%I:%M %p')
        day_name = dbdatetime.strftime("%A")
        date = date_time.split('|')[0]
        time = date_time.split('|')[1]

        print("emaildata------>> ", emaildata, "\n", forum_name, date, time, day_name)

        if sendmail == True:
            print("in email")
            sendDraftMomMail(email_list, forum_name, date, time, Expirydate, day_name)

        if file_data:
            filename = file_data.name
            print(filename, type(filename))

            fs = FileSystemStorage()

            # if (fs.exists(basepath + "static/resources/DraftMom/" + filename)):
            #     fs.delete(basepath + "static/resources/DraftMom/" + filename)
            # file_name = fs.save(basepath + "static/resources/DraftMom/" + filename, file_data)

            if (fs.exists(basepath + "static/resources/" + getFname(fid)  +"/" +mid +"/"+ filename)):
                fs.delete(basepath + "static/resources/" + getFname(fid)  +"/" +mid +"/" + filename)
            file_name = fs.save(basepath + "static/resources/" + getFname(fid)  +"/" +mid +"/"+ filename, file_data)

        meet_query = "Select fid,id from emeet_meeting where title = '" + str(meeting_title) + "'"
        cursor.execute(meet_query)
        fidres = cursor.fetchall()
        print(fidres)

        idarr = []
        for f in fidres:
            fid = f[0]
            idarr.append(fid)
            mid = f[1]
            idarr.append(mid)

        fid = idarr[0]
        mid = idarr[1]

        title_meet = Drafttitle
        d1 = title_meet.split()
        print(d1)
        version1 = d1[2]
        versionres = split(version1)
        version = versionres[1]
        print("version", version)

        approved = "1"
        insertdate = datetime.datetime.now()
        print(insertdate)

        Draftquery1 = "INSERT INTO `emeet_mom1` (`mid`,`pdf`,`fid`,`ver`,`approved`,`insertdate`,`expirydate`,`title`,`FileName`,`status`)" \
                      "values ('" + str(mid) + "','" + str(filename) + "','" + str(fid) + "','" + str(
            version) + "','" + str(approved) + "','" + str(insertdate) + "','" + str(combine) + "','" + str(
            Drafttitle) + "','" + str(filename) + "',1)"

        print("------------=====================----------------------------")
        print(Draftquery1)
        cursor.execute(Draftquery1)

        fetchquery = "Select id from emeet_mom1 where FileName = '" + str(filename) + "' and title ='" + str(
            Drafttitle) + "' and mid='"+ str(mid)+"' and fid='"+ str(fid)+"' "
        cursor.execute(fetchquery)
        id_res = cursor.fetchone()
        momid = id_res[0]

        approve_stat = "Pending"
        for usrid in selectuser:
            getUserid = "Select userid from emeet_manageusers where ename = '" + str(usrid) + "'"
            cursor.execute(getUserid)
            useridres = cursor.fetchone()
            usridres = useridres[0]

            Draftquery10 = "INSERT INTO `emeet_mapping_agenda` (`mom_id`,`userid`,`approve_status`,`InsertDateTime`)" \
                           " values ('" + str(momid) + "','" + str(usridres) + "' ,'" + str(approve_stat) + "','" + str(
                insertdate) + "')"
            print("draft 10 -----------> ", Draftquery10)
            cursor.execute(Draftquery10)

        joined_string = ",".join(selectuser)
        print(joined_string)
        string23 = "Draft MOM uploaded for Meeting ID -" + str(mid) + ",Meeting Title :" + str(
            meeting_title) + ",File Name :" + str(filename) + ",Draft Title :" + str(
            Drafttitle) + ",Access given to UserIds:" + str(joined_string)
        print(string23)

        activityLogs(request, "Draft MOM uploaded for Meeting ID -" + str(mid) + ",Meeting Title :" + str(
            meeting_title) + ",File Name :" + str(filename) + ",Draft Title :" + str(
            Drafttitle) + ",Access given to UserIds:" + str(joined_string))
        jsondata1 = {"status": "success"}

        return HttpResponse(json.dumps(jsondata1, default=str))
    else:
        return redirect(baseURL)


width, height = A4


def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y


def DownloadMeeting(request, id, fname):
    if request.session.has_key('session_key'):
        print("_________________________________________DownloadMeeting Called____________________________________________")
        meeting_title = ""
        id1 = id
        print("id", id1)
        forums = fname
        cursor = connection.cursor()

        # midquery = "Select mid from emeet_meeting where id = '"+str(id1)+"' "
        # cursor.execute(midquery)
        # midres = cursor.fetchone()
        # id = midres[0]

        agenda_response = []

        query = "SELECT ag_id,title,doc,mid,version,aid FROM `emeet_level0` where mid  ='" + str(id1) + "' order by aid"
        cursor.execute(query)
        level0 = cursor.fetchall()
        print(level0)
        agendalen = len(level0)
        if agendalen > 0:
            agenda_ag_id = []
            for li in level0:
                agenda_ag_id.append(li[0])

            query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level1` where parent in (" + str(
                agenda_ag_id).strip(
                '[]') + ") order by aid"
            cursor.execute(query)
            level1 = cursor.fetchall()
            print(level1)
            subagendalen = len(level1)

            subagenda_ag_id = []
            if subagendalen > 0:
                for li in level1:
                    subagenda_ag_id.append(li[0])

                query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level2` where parent in (" + str(
                    subagenda_ag_id).strip('[]') + ") order by aid"
                cursor.execute(query)
                level2 = cursor.fetchall()
                print(level2)
                subsubagendalen = len(level2)
                print(level0)
                print(level1)
                print(level2)
                subsubagenda_ag_id = []
                for li in level2:
                    subsubagenda_ag_id.append(li[0])

            for ag in level0:
                subagendaarr = []

                sss = {}
                ag_title = str(ag[1])
                ag_doc = str(ag[2])

                agenda = {"ag_title": ag_title, "ag_doc": ag_doc}
                sss["agenda"] = agenda

                for sag in level1:
                    if sag[2] == ag[0]:
                        subsubarr = []
                        tmp = getalphaID(sag[5])
                        sag_title = str(ag[5]) + ".(" + tmp + ")" + str(sag[1])
                        sag_doc = str(sag[3])
                        sub_agenda = {"sag_title": sag_title, "sag_doc": sag_doc, "sag_id": sag[0], "said": sag[5]}

                        subagendaarr.append(sub_agenda)
                        sss["sub_agenda"] = subagendaarr
                        for ssag in level2:
                            if ssag[2] == sag[0]:
                                tmp1 = intToRoman(ssag[5])
                                ssag_title = str(ag[5]) + ".(" + tmp + ")" + "(" + tmp1 + ")" + str(ssag[1])
                                ssag_doc = str(ssag[3])
                                subsubagenda = {"ssag_title": ssag_title, "ssag_doc": ssag_doc, "ssag_id": ssag[0],
                                                "said": ssag[5]}
                                subsubarr.append(subsubagenda)
                                sub_agenda['subsubagenda'] = subsubarr

                agenda_response.append(sss)

            # print(agenda_response)
            print("agenda =====>", agenda_response)

            finalpdfarr = []
            for data in agenda_response:
                # print("data===>   ", data)
                # agenda_data\
                for key, value in data.items():
                    if key == 'agenda':
                        agtitle = value['ag_title']
                        print(agtitle)
                        agdoc = value['ag_doc']
                        if len(agdoc) > 0 and agdoc != None:
                            if agdoc.lower().endswith('.pdf'):
                                agendadict = {"agtitle": agtitle, "agdoc": agdoc}
                                finalpdfarr.append(agendadict)

                    elif key == 'sub_agenda':
                        for sag in value:
                            sagtitle = sag['sag_title']
                            print(sagtitle)
                            sagdoc = sag['sag_doc']
                            if len(sagdoc) > 0 and sagdoc != None:
                                if sagdoc.lower().endswith('.pdf'):
                                    subagendadict = {"sagtitle": sagtitle, "sagdoc": sagdoc}
                                    finalpdfarr.append(subagendadict)

                            if 'subsubagenda' in sag.keys():
                                for ssag in sag['subsubagenda']:
                                    ssagtitle = ssag['ssag_title']
                                    print(ssagtitle)

                                    ssagdoc = ssag['ssag_doc']
                                    if len(ssagdoc) > 0 and ssagdoc != None:
                                        if ssagdoc.lower().endswith('.pdf'):
                                            subsubagendadict = {"ssagtitle": ssagtitle, "ssagdoc": ssagdoc}
                                            finalpdfarr.append(subsubagendadict)
                            else:
                                continue

            print("---------------------------------------------------")
            print("finalpdfarr---------------------->",finalpdfarr)

            pdffilepath = resourcesfolderpath + "/" + str(forums) + "/" + str(id1)
            print(pdffilepath)

            pdffile = []
            indextitle = []
            for pdf1 in finalpdfarr:
                for i in pdf1.keys():
                    if "agdoc" in i:
                        val = pdf1[i]
                        pdffile.append(val)
                    elif "sagdoc" in i:
                        pdffile.append(pdf1[i])
                    elif "ssagdoc" in i:
                        pdffile.append(pdf1[i])
                    elif "agtitle" in i:
                        indextitle.append(pdf1[i])
                    elif "sagtitle" in i:
                        indextitle.append(pdf1[i])
                    elif "ssagtitle" in i:
                        indextitle.append(pdf1[i])
                    else:
                        pass

            print("indextitle------->",indextitle)
            print("pdffile--------->",pdffile)

            page_no = []
            for p in pdffile:
                reader = PyPDF2.PdfFileReader(open(pdffilepath + "/" + p, 'rb'))
                NUM_OF_PAGES = reader.getNumPages()
                page_no.append(NUM_OF_PAGES)
            print(page_no)

            count = 0
            indexarr = []
            for i in page_no:
                print(count)
                if count == 0:
                    count += 1
                    indexarr.append(count)
                    count = count + i
                else:
                    indexarr.append(count)
                    count = count + i

            print(indexarr)
            #######################  Create Index
            final_array = [['Sr No.', 'Title', 'Page No.']]
            count = 0
            for i in range(len(indextitle)):
                print(i)
                temp_arr = []
                count = i + 1
                temp_arr.append(str(count))
                temp_arr.append(indextitle[i])
                temp_arr.append(indexarr[i])
                final_array.append(temp_arr)
            print(final_array)

            merger = PdfFileMerger()
            for pdf in pdffile:
                merger.append(open(pdffilepath + "/" + pdf, "rb"))

            with open(pdffilepath + "/Merge.pdf", "wb") as fout:
                merger.write(fout)

            p = "Merge.pdf"

            reader = PyPDF2.PdfFileReader(open(pdffilepath + "/" + p, 'rb'))
            NUM_OF_PAGES = reader.getNumPages()
            print(NUM_OF_PAGES)

            outputStream = open(pdffilepath + "/" + "FinalPagenumber.pdf", "wb")
            output = PdfFileWriter()

            for i in range(NUM_OF_PAGES):
                page_no_pdf = i + 1
                packet = io.BytesIO()
                can = canvas.Canvas(packet)
                can.drawString(225, 20, "Page" + " " + str(page_no_pdf))
                can.save()

                packet.seek(0)
                new_pdf = PdfFileReader(packet)
                existing_pdf = PdfFileReader(open(pdffilepath + "/" + p, "rb"))

                page = existing_pdf.getPage(i)
                page.mergePage(new_pdf.getPage(0))
                output.addPage(page)

                output.write(outputStream)

            outputStream.close()

            cursor = connection.cursor()
            venuequery = "Select dt,venue,title from emeet_meeting where id ='" + str(id1) + "'"
            cursor.execute(venuequery)
            venueres = cursor.fetchall()
            print(venueres)
            for v in venueres:
                dt = v[0]
                venue = str(v[1]).capitalize()
                meeting_title = v[2]

            print("date", dt)
            print("venue", venue)

            meeting_date = dt.date()
            print(meeting_date)

            r = datetime.datetime.strptime(str(meeting_date), '%Y-%m-%d').strftime('%B %d, %Y')

            v = calendar.day_name[dt.weekday()]
            print(v)

            newdate = v + ", " + r
            print(newdate)

            pdf_file = 'index.pdf'

            p = canvas.Canvas(pdffilepath + "/" + pdf_file)
            p.setFont("Times-Roman", 20)
            p.rect(x=40, y=40, width=520, height=760, stroke=1)
            #p.drawString(230, 500, meeting_title)
            p.drawCentredString(4.25 * inch, 500, meeting_title)
            p.setFont("Times-Roman", 16)
            #p.drawString(230, 450, "Venue - " + venue)
            p.drawCentredString(4.25 * inch, 450, "Venue - " + venue)
            p.setFont("Times-Roman", 16)
            #p.drawString(180, 420, "Date -" + newdate)
            p.drawCentredString(4.25 * inch, 420, "Date -" + newdate)
            p.showPage()
            p.setFont("Times-Roman", 20)
            p.drawString(230, 750, "Agenda Index")
            data = final_array
            table = Table(data, colWidths=[2.05 * cm, 12 * cm, 2.8 * cm])

            width, height = A4
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (2, 0), colors.whitesmoke),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                ('TOPPADDING', (0, 0), (-1, 0), 5),
                ('BOTTOMPADDING', (0, 1), (0, -1), 4),
                ('TOPPADDING', (0, 1), (-1, -1), 5),
                ('GRID', (0, 1), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ]))
            table.wrapOn(p, width, height)
            tableheight = len(data)
            print(tableheight)
            t_height = tableheight + 3
            table.drawOn(p, *coord(1.8, t_height, cm))
            p.showPage()
            p.save()

            pdffile1 = ["index.pdf", "FinalPagenumber.pdf"]
            merger = PdfFileMerger()
            for pdf in pdffile1:
                merger.append(open(pdffilepath + "/" + pdf, "rb"))

            with open(pdffilepath + "/" + str(meeting_title) + ".pdf", "wb") as fout:
                merger.write(fout)

            activityLogs(request, "User downloaded " + meeting_title)

            return FileResponse(open(pdffilepath + "/" + str(meeting_title) + ".pdf", 'rb'),
                                content_type="application/pdf", as_attachment=True)
        else:
            return redirect(baseURL + 'manageMeeting/')

    else:
        return redirect(baseURL)


################################################ pushpak #############################################

def orderag(request):
    if request.session.has_key('session_key'):
        print("orderag")
        id = request.POST.get('id')
        print(id)

        cursor = connection.cursor()
        query = "SELECT ag_id,title,aid FROM `emeet_level0` where mid  ='" + str(id) + "' order by aid"
        cursor.execute(query)
        reorderq = cursor.fetchall()
        a = []
        for ele in reorderq:
            a.append(list(ele))
        print(a)

        return JsonResponse({'data': a}, status=200)
    else:
        return redirect(baseURL)


def ordersag(request):
    if request.session.has_key('session_key'):
        print("ordersag")
        id = request.POST.get('id')
        print(id)

        cursor = connection.cursor()
        query = "SELECT ag_id,title,aid FROM `emeet_level1` where parent  ='" + str(id) + "' order by aid"
        cursor.execute(query)
        reorderq = cursor.fetchall()
        a = []
        for ele in reorderq:
            a.append(list(ele))
        print(a)

        return JsonResponse({'data': a}, status=200)
    else:
        return redirect(baseURL)


def orderssag(request):
    if request.session.has_key('session_key'):
        print("orderssag")
        id = request.POST.get('id')
        print(id)

        cursor = connection.cursor()
        query = "SELECT ag_id,title,aid FROM `emeet_level2` where parent  ='" + str(id) + "' order by aid"
        cursor.execute(query)
        reorderq = cursor.fetchall()
        a = []
        for ele in reorderq:
            a.append(list(ele))
        print(a)

        return JsonResponse({'data': a}, status=200)
    else:
        return redirect(baseURL)


def attachment(request, fid, mid, fname):
    if request.session.has_key('session_key'):

        # with open('EmeetingApp/static/resources/board committee/4/dummy.pdf', 'rb') as pdf:
        #     response = HttpResponse(pdf.read(), content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment;filename="dummy.pdf"'
        #     pdf.close()
        #     return response
        print("fname---------->",fname)
        cursor = connection.cursor()
        query = "SELECT fname FROM `emeet_forums` where `fid` =" + str(fid)
        cursor.execute(query)
        foname = cursor.fetchall()
        print(foname[0])
        return FileResponse(
            open('EmeetingApp/static/resources/' + str(foname[0][0]) + '/' + str(mid) + '/' + str(fname), 'rb'),
            content_type="application/pdf")
        # return FileResponse(open('EmeetingApp/static/resources/Board Committee/4/Leave of Absence.pdf', 'rb'), content_type="application/pdf")
    else:
        return redirect(baseURL)


def userslist(request):
    if request.session.has_key('session_key'):
        print("userslist")
        fid = request.POST.get('fid')
        id = request.POST.get('id')
        cursor = connection.cursor()
        query = "SELECT userid,ename FROM `emeet_manageusers` where committee like '%" + str(
            fid) + "%'and access !='admin' and committee !='checker'"
        cursor.execute(query)
        activeuser = cursor.fetchall()
        activeuserarr = []
        activeuseridarr = []
        for i in activeuser:
            activeuserarr.append(i[1])
            activeuseridarr.append(i[0])
        print("active user arr--->",activeuserarr)
        query = "select userid from `emeet_mapping_agendaaccess` where ag_id=" + str(id)
        cursor.execute(query)
        restricteduser = cursor.fetchall()
        restricteduserarr = []
        for i in restricteduser:
            restricteduserarr.append(i[0])

        # paginator = Paginator(comitteedata, 10)
        # page = request.GET.get('page')
        # comitteedata = paginator.get_page(page)
        print(activeuserarr, activeuseridarr)
        data = {'a': activeuserarr, 'b': activeuseridarr, 'restricted': restricteduserarr}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return redirect(baseURL)


def restrictlist(request):
    if request.session.has_key('session_key'):
        print("restrictlist")
        list1 = request.POST.getlist('list1[]')
        list2 = request.POST.getlist('list2[]')
        id = request.POST.get('id')
        cursor = connection.cursor()

        query = "SELECT MAX(id) FROM `emeet_mapping_agendaaccess`"
        cursor.execute(query)
        maxid = cursor.fetchall()
        maxid = maxid[0][0]
        query = "SELECT userid FROM `emeet_mapping_agendaaccess` WHERE `ag_id`='" + str(id) + "'"
        cursor.execute(query)
        resuser = cursor.fetchall()
        print(resuser)
        lli = []
        for usr in resuser:
            lli.append(usr[0])
        print(lli)
        print(list1)
        print(list2)
        for a in list1:
            if a not in lli:
                maxid += 1
                query = "INSERT INTO `emeet_mapping_agendaaccess` (`id`,`ag_id`,`userid`) values (" + str(
                    maxid) + ", " + str(id) + " , '" + a + "')"
                cursor.execute(query)
                print(query)

        for bb in list2:
            if bb in lli:
                maxid += 1
                query = "delete from `emeet_mapping_agendaaccess` where `ag_id` =  " + str(
                    id) + " and `userid`= '" + bb + "'"
                cursor.execute(query)
                print(query)

        return HttpResponse('Updated Successfully')
    else:
        return redirect(baseURL)


def deleteagendas(request):
    if request.session.has_key('session_key'):
        print("deleteagendas")
        ag_id = request.POST.get('ag_id')
        l = request.POST.get('l')
        l = "emeet_level" + l

        cursor = connection.cursor()
        query = "delete  FROM `" + l + "` where `ag_id` =" + ag_id
        print(query)
        cursor.execute(query)
        descr = cursor.fetchall()

        activityLogs(request, "User deleted agenda.")
        return HttpResponse('Deleted Successfully')
    else:
        return redirect(baseURL)


def getdesc(request):
    if request.session.has_key('session_key'):
        print("Meeting info")
        ag_id = request.POST.get('ag_id')
        l = request.POST.get('l')
        l = "emeet_level" + l

        cursor = connection.cursor()
        query = "SELECT descr FROM `" + l + "` where `ag_id` =" + ag_id
        print(query)
        cursor.execute(query)
        descr = cursor.fetchall()

        data = {'descr': descr[0][0]}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return redirect(baseURL)


def updatedesc(request):
    if request.session.has_key('session_key'):
        print("Meeting info")
        ag_id = request.POST.get('ag_id')
        l = request.POST.get('l')
        description = request.POST.get('description')
        l = "emeet_level" + l
        print(ag_id, l, description)
        cursor = connection.cursor()
        query = "update `" + l + "` set `descr` = '" + description + "' where `ag_id` =" + ag_id
        print(query)
        cursor.execute(query)
        descr = cursor.fetchall()

        activityLogs(request, "User updated description.")
        return HttpResponse('Updated Successfully')
    else:
        return redirect(baseURL)


def info(request, id):
    if request.session.has_key('session_key'):
        print("Meeting info")
        cursor = connection.cursor()
        query = "SELECT userid FROM `emeet_manageusers` where access = 'user'"
        cursor.execute(query)
        activeuser = cursor.fetchall()
        activeuserarr = []
        for i in activeuser:
            activeuserarr.append(i[0])

        # paginator = Paginator(comitteedata, 10)
        # page = request.GET.get('page')
        # comitteedata = paginator.get_page(page)
        print(activeuserarr)

        query = "SELECT * FROM `emeet_meeting` where id  ='" + str(id) + "'"
        cursor.execute(query)
        meeting_info = cursor.fetchall()
        meeting_infoarr = []
        print(meeting_info)
        a = {}

        for i in meeting_info:
            s = i[1].strftime('%Y-%m-%d')
            print(s)
            a['date'] = s
            a['Title'] = i[5]
            date_1 = i[1]
            end_date = date_1 + datetime.timedelta(days=i[7])
            print(end_date)
            end = end_date.strftime('%Y-%m-%d')
            a['duration'] = end
            a['hrs'] = i[1].hour
            aa = str(i[1].minute)
            if aa == '0':
                aa = "00"
            a['mins'] = aa
            str1 = i[1].strftime("%H:%M:%S");
            aaa = convert12(str1);
            d = aaa.split("/")
            dat = d[0]
            if int(dat) < 10:
                dat = "0" + dat
            a['hrs'] = dat
            a['Meridian'] = d[1]
            a['id'] = id
            fid = i[2]
        print(a)
        agenda_response = []

        query = "SELECT fname FROM `emeet_forums` where fid  ='" + str(fid) + "'"
        cursor.execute(query)
        forumname = cursor.fetchall()
        print(forumname)

        forum = {'fid': fid, 'fname': forumname[0][0]}

        query = "SELECT ag_id,title,doc,mid,version,aid FROM `emeet_level0` where mid  ='" + str(id) + "' order by aid"
        print("query--->", query)
        cursor.execute(query)
        level0 = cursor.fetchall()
        print(level0)
        agendalen = len(level0)
        if agendalen > 0:
            agenda_ag_id = []
            for li in level0:
                agenda_ag_id.append(li[0])
            print("agenda_ag_id--->", agenda_ag_id)
            query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level1` where parent in (" + str(
                agenda_ag_id).strip('[]') + ") order by aid"
            print("query1---->", query)
            cursor.execute(query)
            level1 = cursor.fetchall()
            print(level1)
            subagendalen = len(level1)

            subagenda_ag_id = []
            if subagendalen > 0:
                for li in level1:
                    subagenda_ag_id.append(li[0])

                query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level2` where parent in (" + str(
                    subagenda_ag_id).strip('[]') + ") order by aid"
                cursor.execute(query)
                level2 = cursor.fetchall()
                print(level2)
                subsubagendalen = len(level2)
                print(level0)
                print(level1)
                print(level2)
                subsubagenda_ag_id = []
                for li in level2:
                    subsubagenda_ag_id.append(li[0])

            for ag in level0:
                subagendaarr = []

                sss = {}
                ag_title = str(ag[5]) + "." + str(ag[1])
                ag_doc = str(ag[2])

                agenda = {"ag_title": ag_title, "ag_doc": ag_doc, "ag_id": ag[0], "aid": ag[5]}
                sss["agenda"] = agenda

                for sag in level1:
                    if sag[2] == ag[0]:
                        subsubarr = []

                        tmp = getalphaID(sag[5])
                        sag_title = str(ag[5]) + ".(" + tmp + ")" + str(sag[1])
                        sag_doc = str(sag[3])
                        sub_agenda = {"sag_title": sag_title, "sag_doc": sag_doc, "sag_id": sag[0], "said": sag[5]}

                        subagendaarr.append(sub_agenda)
                        sss["sub_agenda"] = subagendaarr
                        for ssag in level2:
                            if ssag[2] == sag[0]:
                                tmp1 = intToRoman(ssag[5])
                                ssag_title = str(ag[5]) + ".(" + tmp + ")" + "(" + tmp1 + ")" + str(ssag[1])
                                ssag_doc = str(ssag[3])
                                subsubagenda = {"ssag_title": ssag_title, "ssag_doc": ssag_doc, "ssag_id": ssag[0],
                                                "said": ssag[5]}

                                subsubarr.append(subsubagenda)
                                sub_agenda['subsubagenda'] = subsubarr

                agenda_response.append(sss)

            print(agenda_response)

            print("\nid:------- ", id)
            cursor.execute("SELECT MAX(aid) FROM `emeet_level0` WHERE mid=" + str(id))
            max_angenda_count = cursor.fetchone()[0]
            if max_angenda_count:
                agenda_sr = max_angenda_count + 1
            else:
                agenda_sr = 1
            print("agenda_sr: ", agenda_sr)
            # print(a)

            print("************************************\n")
            # print(a)
            # print("***********************************\n")

            ## meeting details
            cursor.execute("select `dt`,`venue` from `emeet_meeting` where `id`=" + str(id))
            meeting_details = cursor.fetchone()
            print('meeting_details-->  ', meeting_details)
            date = datetime.datetime.strptime(str(meeting_details[0]), "%Y-%m-%d  %H:%M:%S")
            date_time = date.strftime("%d-%m-%Y %I:%M%p")
            meet_date = date_time.split(" ")[0]
            meet_time = date_time.split(" ")[1]
            meet_venue = meeting_details[1]
            print(meet_venue, meet_date, meet_time)

            name = "{0}".format(request.session.get('ename'))
            date_time = "{0}".format(request.session.get('date_time'))
            response = name + " " + date_time

            return render(request, "info.html",
                          {'baseURL': baseURL, 'activeuserarr': activeuserarr, 'info': a, 'agenda_sr': agenda_sr,
                           'venue': meet_venue, 'date': meet_date, 'time': meet_time,
                           'agenda_response': agenda_response, 'forum': forum, "flag": "True", 'response': response})
        else:
            print("\nelse id:------->> ", id)
            cursor.execute("SELECT MAX(aid) FROM `emeet_level0` WHERE mid=" + str(id))
            max_angenda_count = cursor.fetchone()[0]
            if max_angenda_count:
                agenda_sr = max_angenda_count + 1
            else:
                agenda_sr = 1
            print("agenda_sr: ", agenda_sr)
            # print(a)

            cursor.execute("select `dt`,`venue` from `emeet_meeting` where `id`=" + str(id))
            meeting_details = cursor.fetchone()
            print('meeting_details-->  ', meeting_details)
            date = datetime.datetime.strptime(str(meeting_details[0]), "%Y-%m-%d  %H:%M:%S")
            date_time = date.strftime("%d-%m-%Y %I:%M%p")
            meet_date = date_time.split(" ")[0]
            meet_time = date_time.split(" ")[1]
            meet_venue = meeting_details[1]
            print(meet_venue, meet_date, meet_time)

            name = "{0}".format(request.session.get('ename'))
            date_time = "{0}".format(request.session.get('date_time'))
            response = name + " " + date_time
            return render(request, "info.html",
                          {'baseURL': baseURL, 'activeuserarr': activeuserarr, 'info': a, 'venue': meet_venue,
                           'date': meet_date, 'time': meet_time,
                           'forum': forum, "flag": "False", 'response': response, 'agenda_sr': agenda_sr})
    else:
        return redirect(baseURL)

    # return render(request, "info.html",{'baseURL':baseURL,'forum':forum,'activeuserarr':activeuserarr,'info':a,'agenda_response':agenda_response})


def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundereds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundereds +
           tens + ones)

    return ans.lower();


def getalphaID(i):
    # alphabets = ["0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh", "ii", "jj", "kk", "ll", "mm", "nn", "oo", "pp", "qq", "rr", "ss", "tt", "uu", "vv", "ww", "xx", "yy", "zz" ];
    # return alphabets[i]
    alphabets = ["0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                 "t", "u", "v", "w", "x", "y", "z", "aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh", "ii", "jj",
                 "kk", "ll", "mm", "nn", "oo", "pp", "qq", "rr", "ss", "tt", "uu", "vv", "ww", "xx", "yy", "zz"];
    if type(i) == int:
        return alphabets[i]
    elif type(i) == str:
        return alphabets.index(i)


def updateinfo(request):
    if request.session.has_key('session_key'):
        print("Update Board Committee information")
        id = request.POST.get('id')
        print(id)
        Title = request.POST.get('Title')
        print(Title)
        datee = request.POST.get('datee')
        print(datee)
        Expiry_date = request.POST.get('Expiry_date')
        print(Expiry_date)
        hrs = request.POST.get('hrs')
        print(hrs)
        mins = request.POST.get('mins')
        print(mins)
        meridian = request.POST.get('meridian')
        print(meridian)
        da = datee + " " + hrs + ":" + mins + ":00 " + meridian
        print(da)
        date = datetime.datetime.strptime(da, '%Y-%m-%d %I:%M:%S %p')
        date = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
        print(date)
        Expiry_date = datetime.datetime.strptime(Expiry_date, '%Y-%m-%d')
        actual_date = datetime.datetime.strptime(datee, '%Y-%m-%d')

        nodays = str((Expiry_date - actual_date).days)
        cursor = connection.cursor()
        query = "update emeet_meeting set title='" + Title + "',dt='" + date + "',days='" + nodays + "' where id ='" + id + "';"
        cursor.execute(query)

        activityLogs(request, 'User updated ' + Title)
        return HttpResponse("Updated succesfully..")
    else:
        return redirect(baseURL)


def reorderag(request):
    if request.session.has_key('session_key'):
        print("reorderag")
        id = request.POST.get('id')
        aglist = request.POST.getlist('aglist[]')
        ailist = request.POST.getlist('ailist[]')
        print(aglist)
        print(ailist)
        print(id)
        print(request.body)
        sam = ""
        for indx, aglis in enumerate(aglist):
            print(aglis, indx)
            sam = sam + " when ag_id='" + str(aglis) + "' then " + str(indx + 1)
        print(sam)
        cursor = connection.cursor()
        query = "UPDATE emeet_level0 SET aid = (case " + sam + " end) where ag_id in (" + ','.join(aglist) + ")"
        print(query)
        cursor.execute(query)

        return HttpResponse("Updated Successfully")
    else:
        return redirect(baseURL)


def reordersag(request):
    if request.session.has_key('session_key'):
        print("reordersag")
        id = request.POST.get('id')
        saglist = request.POST.getlist('saglist[]')
        sailist = request.POST.getlist('sailist[]')
        print(saglist)
        print(sailist)
        print(id)
        print(request.body)
        sam = ""
        for indx, saglis in enumerate(saglist):
            print(saglis, indx)
            sam = sam + " when ag_id='" + str(saglis) + "' then " + str(indx + 1)
        print(sam)
        cursor = connection.cursor()
        query = "UPDATE emeet_level1 SET aid = (case " + sam + " end) where ag_id in (" + ','.join(saglist) + ")"
        print(query)
        cursor.execute(query)

        return HttpResponse("Updated Successfully")
    else:
        return redirect(baseURL)


def reorderssag(request):
    if request.session.has_key('session_key'):
        print("reorderssag")
        id = request.POST.get('id')
        ssaglist = request.POST.getlist('ssaglist[]')
        ssailist = request.POST.getlist('ssailist[]')
        print(ssaglist)
        print(ssailist)
        print(id)
        print(request.body)
        sam = ""
        for indx, ssaglis in enumerate(ssaglist):
            print(ssaglis, indx)
            sam = sam + " when ag_id='" + str(ssaglis) + "' then " + str(indx + 1)
        print(sam)
        cursor = connection.cursor()
        query = "UPDATE emeet_level2 SET aid = (case " + sam + " end) where ag_id in (" + ','.join(ssaglist) + ")"
        print(query)
        cursor.execute(query)

        return HttpResponse("Updated Successfully")
    else:
        return redirect(baseURL)


def convert12(str1):
    # Get Hours
    print("------------", str1)
    h1 = ord(str1[0]) - ord('0');
    h2 = ord(str1[1]) - ord('0');

    hh = h1 * 10 + h2;

    # Finding out the Meridien of time
    # ie. AM or PM
    Meridien = "";
    if (hh < 12):
        Meridien = "AM";
    else:
        Meridien = "PM";

    hh %= 12;

    # Handle 00 and 12 case separately
    if (hh == 0):
        hh = '12'
        print("12", end="");

        # Printing minutes and seconds


    else:
        print(hh, end="");

        # Printing minutes and seconds
        for i in range(2, 8):
            print(str1[i], end="");

            # After time is printed
    # cout Meridien
    return str(hh) + "/" + Meridien


def fetchagenda(request):
    print("fetchagenda")
    ag_id = request.POST.get('ag_id')
    l = request.POST.get('l')
    l1 = request.POST.get('l')
    l = "emeet_level" + l

    cursor = connection.cursor()
    query = "SELECT aid,title,descr,ColorId,doc FROM `" + l + "` where `ag_id` =" + ag_id
    print(query)
    cursor.execute(query)
    fdata = cursor.fetchall()
    data = {}
    if l == "emeet_level1":
        aid = fdata[0][0]
        aid = getalphaID(aid)
    elif l == "emeet_level2":
        aid = fdata[0][0]
        aid = intToRoman(aid)
    else:
        aid = fdata[0][0]
    data['aid'] = aid
    data['title'] = fdata[0][1]
    data['descr'] = fdata[0][2]
    data['ColorId'] = fdata[0][3]
    data['doc'] = fdata[0][4]
    data['ag_id'] = ag_id
    data['l'] = l1
    print(data)

    return HttpResponse(json.dumps(data), content_type='application/json')


def updateagendas(request):
    file_data = request.FILES.get('file')
    data = request.POST.get('requestData')
    request_data = json.loads(data)
    if file_data:
        print(file_data.name)
    print(request_data, type(request_data))

    agenda_title = request_data['title']
    agenda_desc = request_data['desc']
    item_type = request_data['itype']
    committee = request_data['commitee']
    mid = request_data['mid']
    id = request_data['id']
    aid = request_data['aid']
    l = request_data['l']

    print(id, ' | ', l, ' | ', agenda_title, ' | ', agenda_desc, ' | ', item_type, '\n')
    cursor = connection.cursor()
    if file_data:
        filename = file_data.name
        print(filename, type(filename))
        fs = FileSystemStorage()
        if file_data != None:
            # pass
            print("=============================" + basepath + "/static/resources/" + committee + "/" + str(
                mid) + "/" + filename)
            if (fs.exists(basepath + "/static/resources/" + committee + "/" + str(mid) + "/" + filename)):
                filename = "lvl" + str(l) + "_" + str(aid) + "_" + filename
                fs.save(basepath + "/static/resources/" + committee + "/" + str(mid) + "/" + filename, file_data)
            else:
                file_name = fs.save(basepath + "/static/resources/" + committee + "/" + str(mid) + "/" + filename,
                                    file_data)
    else:
        filename = ''
    query = "update emeet_level" + str(l) + " set title='" + agenda_title + "',descr='" + str(
        agenda_desc) + "',ColorId=" + str(item_type) + ",doc='" + filename + "' " \
                                                                             "where ag_id ='" + str(id) + "';"
    print(query)
    cursor.execute(query)

    return HttpResponse(json.dumps(data), content_type='application/json')


def removefile(request):
    id = request.POST.get('id')
    l = request.POST.get('l')
    commitee = request.POST.get('commitee')
    mid = request.POST.get('mid')
    aid = request.POST.get('aid')
    f = request.POST.get('f')
    fs = FileSystemStorage()

    # pass

    cursor = connection.cursor()
    query = "update emeet_level" + str(l) + " set doc='' where ag_id ='" + str(id) + "';"
    print(query)
    cursor.execute(query)
    fs.delete(basepath + "/static/resources/" + commitee + "/" + str(mid) + "/" + f)

    return HttpResponse("Success")


def uploadZip(request):
    file_data = request.FILES.get('file')
    data = request.POST.get('requestData')
    request_data = json.loads(data)
    if file_data:
        print(file_data.name)
    fs = FileSystemStorage()
    print(request_data, type(request_data))


    if file_data != None:
        # pass
        currentdate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        filename = currentdate
        fs.save(basepath + "static/temp/" + filename + ".zip", file_data)





    with ZipFile(basepath + "static/temp/" + filename + ".zip", 'r') as zip:
        zip.printdir()
        print("namelist-------->",zip.namelist())

        agendacsv = ''
        zipfile_extli = []
        for f in zip.namelist():

            if f.lower().endswith(('.pdf','.ppt','.docx','.doc','.txt','.xls')):
                zipfile_extli.append('validfile')
            elif f.lower().endswith('.csv'):
                if f.lower().__contains__('agenda.csv'):
                    zipfile_extli.append('csv')
                    agendacsv = f

                else:
                    zipfile_extli.append('false')
            else:
                zipfile_extli.append('false')


        if all(x in zipfile_extli for x in ['validfile','csv']):
            print("valid file")
        else:
            context_data = {'message': 'Please choose correct file.'}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")


        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall(basepath + "static/temp/" + filename + "/")

        print('Done!')
        zip.close()
    id = request_data['id']
    mid = request_data['mid']
    fid = request_data['fid']
    commitee = request_data['commitee']

    naturelist = {
        "Approval": 1,
        "Information": 2,
        "Discussion": 3,
        "Presentation": 4,
        "Noting": 5,
        "Consideration": 6,
        "Ratification": 7,
        "Other": 8
    }
    print("agendacsv---------->", agendacsv)
    if (fs.exists(basepath + "/static/resources/" + commitee + "/" + str(mid))):
        fs.delete(basepath + "/static/resources/" + commitee + "/" + str(mid))

    shutil.copytree(basepath + "static/temp/" + filename + "/",
                    basepath + "/static/resources/" + commitee + "/" + str(mid) + "/",
                    ignore=shutil.ignore_patterns('*.csv'))

    #with open(basepath + "static/temp/" + filename + "/Agenda.csv", newline='') as csvfile:
    with open(basepath + "static/temp/" + filename + "/"+agendacsv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        data = list(spamreader)
        data.pop(0)
        # for row in spamreader:
        # for ele in row:
        #     print(ele)
        #
        # id = row[0]
        # title =row[1]
        # doc =row[2]
        # natur =row[3]
        # print(">>>>",id,">>>>",title,">>>>",doc,">>>>",natur)
        data = sorted(data)
        print(data)
        aid = 1
        said = 1
        ssaid = 1
        for a in data:

            id = a[0].split('.')
            if len(id) == 1:
                agid = id[0]
                date = '2020-10-13 00:00:00.000'
                cursor = connection.cursor()
                cursor.execute(
                    "insert into `emeet_level0` (`title`,`descr`,`fid`,`doc`,`mid`,`version`,`aid`,`dt1`,`dt2`,`ColorId`)"
                    "values('" + a[1] + "','','" + str(fid) + "','" + a[2] + "','" + str(
                        mid) + "','0','" + str(aid) + "','" + date + "',""'" + date + "','" + str(
                        naturelist["" + a[3]]) + "')")
                ag_idr = cursor.lastrowid
                aid = aid + 1
                said = 1
                print("level0", a[1])
            if len(id) == 2:
                subagid = id[1]
                cursor = connection.cursor()
                cursor.execute("insert into `emeet_level1` (`title`,`descr`,`parent`,`doc`,`version`,`aid`,`ColorId`)"
                               "values('" + a[1] + "','','" + str(ag_idr) + "','" + a[2] + "','0','" + str(
                    said) + "','" + str(naturelist["" + a[3]]) + "')")
                sag_idr = cursor.lastrowid
                said = said + 1
                ssaid = 1
                print("level1", a[1])
            if len(id) == 3:
                subsubagid = id[2]
                cursor = connection.cursor()
                cursor.execute("insert into `emeet_level2` (`title`,`descr`,`parent`,`doc`,`version`,`aid`,`ColorId`)"
                               "values('" + a[1] + "','','" + str(sag_idr) + "','" + a[2] + "','0','" + str(
                    ssaid) + "','" + str(
                    naturelist["" + a[3]]) + "')")
                ssag_idr = cursor.lastrowid
                ssaid = ssaid + 1
                print("level2", a[1])

    csvfile.close()
    print(id)
    print(mid)
    fs.delete(basepath + "static/temp/" + filename + ".zip")

    shutil.rmtree(basepath + "static/temp/" + filename, ignore_errors=True)
    return HttpResponse("Upload Success")


def downloadAttendanceReport(request, fid):
    cursor = connection.cursor()
    committee = request.GET.get('committee')

    # if committee == None or committee == 'all':
    #     pass
    # else:
    cursor.execute('select `fname` from `emeet_forums` where fid=' + str(fid))
    forum = cursor.fetchone()[0]
    print('forum-------> ', forum)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + forum + '.csv'

    query = "SELECT `userid`,`ename` from `emeet_manageusers` WHERE committee like '%" + str(
        fid) + "%' and `access`='user' "
    cursor.execute(query)
    users = cursor.fetchall()
    print("users =========> ", users)

    # for usr in users:
    #     cursor.execute("select `mid`,`userid`,`status` from `emeet_attend` where `fid` = '"+committee+"'and `remarks`='Marked' "
    #       "and `userid` = '"+usr+"' ")

    cursor.execute("select `title`,`dt`,`id` from `emeet_meeting` where fid = " + str(fid))
    meetings = cursor.fetchall()
    print("meetings =======> ", meetings)

    print(cursor.execute(
        "select `mid`,`userid`,`status` from `emeet_attend` where `fid` = '" + str(fid) + "'and `remarks`='Marked' "))
    marked_users = cursor.fetchall()
    print('marked_users ====>> ', marked_users)

    att = []
    for aele in marked_users:
        att.append(aele[0])
    tbl = []
    for usr in users:
        entry = []
        entry.append(usr[0])
        entry.append(usr[1])
        for meet in meetings:
            for mkdu in marked_users:

                #print(mkdu[0], meet[2], usr[0], mkdu[1])
                if str(mkdu[0]) == str(meet[2]) and usr[0] == mkdu[1]:
                    #print("inside")
                    if mkdu[2] == 'true':
                        entry.append('Present')
                    elif mkdu[2] == 'false':
                        entry.append('Absent')

                    break
            else:

                if str(meet[2]) in att:
                    #print("infalse")
                    # entry.append('false')
                    entry.append("Not Marked")
                else:
                    # entry.append("disabled")
                    entry.append("Not Marked")
        tbl.append(entry)
        #print(entry)
    print('tbl----->',tbl)

    cursor.close()
    writer = csv.writer(response)
    field_list = ['UserId', 'User']
    for idx, meet in enumerate(meetings):
        meeting = str(idx + 1) + '.' + meet[0] + ' [' + (meet[1]).strftime("%d/%m/%Y %I:%M:%S %p") + ']'
        #print(meeting)
        field_list.append(meeting)

    writer.writerow(field_list)

    for field in field_list:
        for data in tbl:
            # data = list(data)
            #print(data)
            # field = data[0]
            #
            # # print(list(users))
            # data.remove(data[0])
            writer.writerow(data)
        break
        #     list(users).remove(data[0])
        # field_list.remove(field)

        # dt = data[2]
        # venue = data[3]
        # data = tuple(data)
        # writer.writerow([field])
    # name = "{0}".format(request.session.get('ename'))
    # activityLogs(request, "User " + name + " have download activity logs data.")
    return response


def markattendance(request):
    if request.session.has_key('session_key'):
        mid = request.POST.get('mid')
        fid = request.POST.get('fid')
        uid = request.POST.get('uid')
        status = request.POST.get('status')
        cursor = connection.cursor()

        cursor.execute("select id from `emeet_attend` where `mid` = '" + mid + "' and `userid` = '" + uid + "' ")
        list1 = cursor.fetchall()

        if len(list1) == 0:
            cursor.execute("insert into `emeet_attend`(`mid`, `userid`, `status`, `fid`, `dt`,`remarks`) "
                           "VALUES ('" + mid + "','" + uid + "','" + status + "','" + fid + "','" + str(
                datetime.datetime.now()) + "','Marked')")
            list111 = cursor.fetchall()
        else:
            cursor.execute(
                "update `emeet_attend` set  `status` = '" + status + "' where id = '" + str(list1[0][0]) + "'")
            list1111 = cursor.fetchall()
        return HttpResponse(fid)
    else:
        return redirect(baseURL)


def attendance(request):
    if request.session.has_key('session_key'):
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))

        response = name + " " + date_time
        print(response)
        print("----------- attendance -----------")
        cursor = connection.cursor()

        cursor.execute("select `fid`,`fname` from `emeet_forums` where `approved` = 'approved' and stat = 'True' or stat = 'true' ")
        committee_list = cursor.fetchall()
        committee_data = []
        for commdata in committee_list:
            committee_data.append(commdata)

        committee_dict = dict(committee_data)
        print('committee_dict==============>> ', committee_dict)

        if request.method == 'GET':

            committee = request.GET.get('committee')
            print("com-- ", committee, type(committee))
            if (committee == None) or (committee == 'all'):
                committee = '1'
            else:
                committee = request.GET.get('committee')
            query = "SELECT `userid`,`ename` from `emeet_manageusers` WHERE committee like '%" + committee + "%' and `access`='user' "
            cursor.execute(query)
            users = cursor.fetchall()
            print("users =========> ", users)

            cursor.execute("select `title`,`dt`,`id` from `emeet_meeting` where fid = " + committee)
            meetings = cursor.fetchall()

            print("meetings =======> ", meetings)
            meetings1 = meetings
            seq = {}

            counter = 1
            for m in meetings:
                seq[counter] = m[2]

                counter = counter + 1

            print("_)))))))))))))))))))____________________", seq)
            cursor.execute(
                "select `mid`,`userid`,`status` from `emeet_attend` where `fid` = '" + committee + "'and `remarks`='Marked' ")
            marked_users = cursor.fetchall()
            print('marked_users ====>> ', marked_users)
            att = []
            for aele in marked_users:
                att.append(aele[0])
            tbl = []
            print("ZZZZZZZZZZZZZZZZZZZZZZZ111111111111111111")
            for usr in users:
                print("ZZZZZZZZZZZZZZZZZZZZZZZ")
                entry = []
                entry.append(usr[0])
                entry.append(usr[1])
                for meet in meetings:
                    for mkdu in marked_users:

                        print(mkdu[0], meet[2], usr[0], mkdu[1])
                        if str(mkdu[0]) == str(meet[2]) and usr[0] == mkdu[1]:
                            print("inside")
                            entry.append(mkdu[2])

                            break
                    else:

                        if str(meet[2]) in att:
                            print("infalse")
                            entry.append('false')

                        else:
                            entry.append("disabled")

                tbl.append(entry)
                print(entry)
            print(tbl)
            print("-------------------", users)
            return render(request, 'attendance.html',
                          {'baseURL': baseURL, 'response': response, 'committee_dict': committee_dict, 'users': users,
                           'meetings': meetings, 'meetings1': meetings1, 'fid': committee, 'marked_users': marked_users,
                           'tbl': tbl, 'seq': json.dumps(seq)})

        elif request.method == 'POST':
            committee = request.POST.get('committee')
            menu = request.POST.get('menu')
            query = "SELECT `userid`,`ename` from `emeet_manageusers` WHERE committee like '%" + committee + "%' and `access`='user' "
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.execute("select `title`,`dt`,`id` from `emeet_meeting` where fid = " + committee)
            meetings1 = cursor.fetchall()

            print("meetings =======> ", meetings1)

            if menu:
                if menu == 'Date':
                    start_date = request.POST.get('startdate')
                    end_date = request.POST.get('enddate')
                    print(start_date, ' | ', end_date)

                    cursor.execute(
                        "select `title`,`dt`,`id` from `emeet_meeting` where fid =  '" + committee + "' and `dt` "
                                                                                                     "between '" + start_date + "' and '" + end_date + "' ")

                    # Meeting.objects.filter(fid=fidres, dt__range=(stat_convert, end_convert)).order_by('dt')
                    meetings = cursor.fetchall()
                    print("search meetings =======> ", meetings)
                    seq = {}
                    counter = 1
                    for m in meetings:
                        seq[counter] = m[2]
                        counter = counter + 1

                elif menu == 'Meeting_Title':
                    title = request.POST.get('title')
                    # cursor.execute(
                    #     "select `title` from `emeet_meeting` where fid =  '" + committee + "' and `id`='" + title + "' ")

                    cursor.execute(
                        "select `title`,`dt`,`id` from `emeet_meeting` where fid =  '" + committee + "' and `id`='" + title + "' ")
                    meetings = cursor.fetchall()
                    print("search meetings =======> ", meetings)
                    seq = {}
                    counter = 1
                    for m in meetings:
                        seq[counter] = m[2]
                        counter = counter + 1
            cursor.execute(
                "select `mid`,`userid`,`status` from `emeet_attend` where `fid` = '" + committee + "'and `remarks`='Marked' ")
            marked_users = cursor.fetchall()
            print('marked_users ====>> ', marked_users)
            att = []
            for aele in marked_users:
                att.append(aele[0])
            tbl = []
            for usr in users:
                entry = []
                entry.append(usr[0])
                entry.append(usr[1])
                for meet in meetings:
                    for mkdu in marked_users:

                        print(mkdu[0], meet[2], usr[0], mkdu[1])
                        if str(mkdu[0]) == str(meet[2]) and usr[0] == mkdu[1]:
                            print("inside")
                            entry.append(mkdu[2])

                            break
                    else:

                        if str(meet[2]) in att:
                            print("infalse")
                            entry.append('false')

                        else:
                            entry.append("disabled")

                tbl.append(entry)
                print(entry)
            print(tbl)

            return render(request, 'attendance.html',
                          {'baseURL': baseURL, 'response': response, 'committee_dict': committee_dict, 'users': users,
                           'meetings': meetings, 'meetings1': meetings1, 'fid': committee, 'marked_users': marked_users,
                           'tbl': tbl, 'seq': json.dumps(seq)})
    else:
        return redirect(baseURL)


# ################################## Vedanti ########################################
#
# basepath = 'C:/Users/VEDANTI/PycharmProjects/Emeeting/EmeetingApp/'
#
def create_captcha():
    print("in def")
    captcha_text = ''.join(random.choices(string.ascii_lowercase, k=2)).join(random.choices(string.digits, k=2))
    print(captcha_text)

    # img = Image.open('EmeetingApp/static/images/captcha.png')
    # d1 = ImageDraw.Draw(img)
    # d1.text((0, 0), captcha_text,  fill=(0, 0, 153))
    # #img.show()
    # fs = FileSystemStorage()
    #
    # if (fs.exists('EmeetingApp/static/images/captcha111.png')):
    #     fs.delete('EmeetingApp/static/images/captcha111.png')
    # img.save("EmeetingApp/static/images/captcha111.png")
    #
    # image_captcha = ImageCaptcha()
    # image_captcha.generate_image(captcha_text)
    # image_file = "EmeetingApp/static/images/captcha_image.png"
    # image_captcha.write(captcha_text, image_file)
    return captcha_text


def loginpage(request):
    if request.session.has_key('session_key'):
        return redirect(baseURL + 'manageMeeting/', {'baseURL': baseURL})

    captcha_text = create_captcha()
    return render(request, 'login.html', {'baseURL': baseURL, 'captcha_text': captcha_text})


# username =  mobitrail_user
# passwrd = mobi@123

def login(request):
    char_set = string.ascii_uppercase + string.digits
    session_key = ''.join(random.sample(char_set * 20, 20))
    print(session_key)

    if request.method == "POST":
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        usercaptcha = request.POST.get('usercaptcha')
        captcha_text = request.POST.get('captcha_text')
        print('captcha_text: ', captcha_text)
        print("\nuser: ", userName, ',', password, ',', usercaptcha)
        pass_wrd = password.encode('utf-8')

        enc_pass = encryption(pass_wrd)
        # print('enc_pass: ',enc_pass,len(enc_pass))

        cursor = connection.cursor()

        last_login = datetime.datetime.now()
        print("last login---->", last_login)
        cursor.execute(
            "update `emeet_manageusers` set `LUA`= '" + str(last_login) + "' where userid = '" + userName + "' ")

        pass_query = "select `pwd`,`ename`,`LUA`,`access`,`active` from emeet_manageusers where userid='" + userName + "'  "
        # print(pass_query)
        try:
            print("in try")
            cursor.execute(pass_query)
            passwrd = cursor.fetchall()
            print('passwrd------------->> ', passwrd, len(passwrd))

            if len(passwrd) == 0:
                print("Invalid user")
                captcha_text = create_captcha()
                context_data = {'captcha_text': captcha_text, 'message': 'Invalid User Name or Password'}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

            else:
                active_status = passwrd[0][4]
                print('active_status---------> ', active_status)

                if active_status.lower() == 'false':
                    print("disable user")
                    captcha_text = create_captcha()
                    msg = 'You account is locked, Kindly contact Secretarial Team.'
                    context_data = {'userName': userName, 'password': password, 'captcha_text': captcha_text,
                                    'message': msg}
                    return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

                elif active_status.lower() == 'true':
                    pwd = passwrd[0][0]
                    ename = passwrd[0][1]
                    dateTime = (passwrd[0][2]).strftime("%d/%m/%Y %I:%M %p")
                    userType = passwrd[0][3]
                    print('============', pwd, ename, dateTime, userType)

                    # print('pwd: ',pwd,len(pwd))
                    pwd = pwd.encode('utf-8')
                    print(decryption(pwd))

                    if (decryption(pwd) == decryption(enc_pass)) and (usercaptcha == captcha_text):
                        print(decryption(pwd), "===", decryption(enc_pass))
                        print("valid user")

                        request.session['userid'] = userName
                        request.session['ename'] = ename
                        request.session['date_time'] = dateTime
                        request.session['user_type'] = userType
                        request.session['session_key'] = session_key

                        name = "{0}".format(request.session.get('ename'))
                        print(name)
                        activityLogs(request, "User " + name + " have logged in.")
                        return redirect(baseURL + 'manageMeeting/')

                    elif usercaptcha != captcha_text:
                        print("Invalid captcha")
                        captcha_text = create_captcha()
                        context_data = {'userName': userName, 'password': password, 'captcha_text': captcha_text,
                                        'message': 'Invalid Captcha'}
                        return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

                    else:
                        print("Invalid user")
                        captcha_text = create_captcha()
                        context_data = {'captcha_text': captcha_text, 'message': 'Invalid User Name or Password'}
                        return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")


        except Exception as e:
            print("exct---> ", e)
            return redirect(baseURL)


def logout(request):
    print("logout")
    name = "{0}".format(request.session.get('ename'))
    activityLogs(request, "User " + name + " have logged out.")
    del request.session['session_key']
    return redirect(baseURL)


def activityLogs(request, activity):
    if request.session.has_key('session_key'):
        ename = "{0}".format(request.session.get('ename'))
        user_type = "{0}".format(request.session.get('user_type'))
        date = datetime.datetime.now()
        print("logs date---->",date)
        # .strftime("%Y-%m-%d %H:%M:%S")
        # add_activity = EmeetCmslogs(userid=ename,user=user_type,activity=activity,dt=date)
        cursor = connection.cursor()
        query = "insert into `emeet_cmslogs` (`activity`,`dt`,`user`,`userid`) values('" + activity + "','" + str(
            date) + "','" + user_type + "','" + ename + "')"
        print(query)
        cursor.execute(query)
    else:
        return redirect(baseURL)


def manageActivityLogs(request):
    if request.session.has_key('session_key'):
        activities = EmeetCmslogs.objects.all().order_by('-id')
        datalength = len(activities)
        paginator = Paginator(activities, 15)
        page = request.GET.get('page')
        activities = paginator.get_page(page)

        li = []
        print("cmslogs----->",activities)
        for a in activities:
            date_db = (a.dt).strftime("%d/%m/%Y %I:%M %p")
            li.append(date_db)
        activities1 = zip(activities, li)

        # response = "Welcome,"
        # if request.session.get('name'):
        #     print("Enter Username")
        #     response += " {0}".format(request.session.get('name'))
        #     print(response)
        #     usertype = "{0}".format(request.session.get('usertype')).lower()
        #     user_rights = "{0}".format(request.session.get('rights')).lower()

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        return render(request, 'activity_logs.html',
                      {'baseURL': baseURL, 'activities':activities,'activities1': activities1, 'datalength': datalength, 'response': response})
    else:
        return redirect(baseURL)


def DownloadLogsdata(request):
    print("Download Activity logs")
    if request.session.has_key('session_key'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Logs_Master.csv"'
        cursor = connection.cursor()
        q = "SELECT  `activity`,`dt`,`user` FROM emeet_cmslogs "

        cursor.execute(q)
        notifications = cursor.fetchall()
        cursor.close()
        writer = csv.writer(response)
        writer.writerow(['Activity', 'Date', 'User'])
        for data in notifications:
            print(data)
            act = data[0]
            dt = data[1]
            usr = data[2]
            dt = dt.strftime("%m/%d/%Y %I:%M:%S %p")
            data = tuple(data)
            writer.writerow([act, dt, usr])
        name = "{0}".format(request.session.get('name'))
        # activityLogs(request, "User <b>" + name + "</b> have download activity logs data.")
        return response
    else:
        return redirect(baseURL)


def changePassword(request):
    name = "{0}".format(request.session.get('ename'))
    date_time = "{0}".format(request.session.get('date_time'))
    response = name + " " + date_time
    print("change pass name: ", name)
    return render(request, 'change_pass.html', {'baseURL': baseURL, 'response': response})


def changeUserPass(request):
    print("============= change pass ==================")
    cursor = connection.cursor()
    userid = "{0}".format(request.session.get('userid'))

    oldpass = request.POST.get('oldpass')
    newpass = request.POST.get('newpass')
    confirmpass = request.POST.get('confirmpass')
    print(oldpass, newpass, confirmpass)

    newpass_wrd = newpass.encode('utf-8')

    enc_newpass = encryption(newpass_wrd)
    print("enc new pass: ", enc_newpass)
    enc_passwd = enc_newpass.decode('utf-8')
    print(enc_passwd)

    currentdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(currentdate)

    cursor = connection.cursor()
    cursor.execute("update `emeet_manageusers` set `pwd`='" + enc_passwd + "',`pwd_dt`='" + str(
        currentdate) + "' where `userid`='" + userid + "' ")
    print("pass changed!")
    # return HttpResponse(baseURL)

    return redirect(baseURL + "manageMeeting/")


def changeAccStatus(request):
    print('=============  acc status ====================')
    userid = request.POST.get('userid')
    print('user: ', userid)

    cursor = connection.cursor()
    cursor.execute("update `emeet_manageusers` set `accountStatus` = 'True' where `userid`='" + userid + "' ")
    print("acc status changed")
    return redirect(baseURL + 'manageUser')


########################## User Management ######################
################## user management ###########################
def manageUser(request):
    print("+++++++++++++++++manageUSer Called+++++++++++++++++++++++++")

    commitee = request.GET.get('commitee')
    usertype = request.GET.get('usertype')
    display = request.GET.get('display')
    txt = request.GET.get('txt')
    print("commitee====>", commitee, " | usertype====>", usertype, " | display======>", display, " | txt============>",
          txt)
    cursor = connection.cursor()
    query = ""
    cmsflag = ""
    if usertype == "1":
        cmsflag = 'True'
    elif usertype == "2":
        cmsflag = 'False'

    if commitee == None or commitee == 0 and usertype == None and display == None and txt == None :
        query = " select * from emeet_manageusers WHERE access!='superadmin'"
        print("query===", query)
    elif commitee == '0' and usertype == '0' and display == '10' and txt == '':
        query = " select * from emeet_manageusers WHERE access!='superadmin'"
        print("query 0 ===", query)

    # ***************************************commitee with combination******************************************
    elif commitee != '0' and usertype == '0' and display == '10' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and find_in_set(" + commitee + ",committee) LIMIT 20"
        print("query 1 =======", query)

    elif commitee != '0' and usertype != '0' and display == '10' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and find_in_set(" + commitee + ",committee) and cmsflag='" + cmsflag + "' LIMIT 20"
        print("query 2 ======", query)


    elif commitee != '0' and usertype != '0' and display != '' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and find_in_set(" + commitee + ",committee) and cmsflag='" + cmsflag + "' LIMIT " + display
        print("query 3 =====", query)
    elif commitee != '0' and usertype != '0' and display != '' and txt != '':
        query = "select * from emeet_manageusers where access!='superadmin' and find_in_set(" + commitee + ",committee) and cmsflag='" + cmsflag + "' and userid='" + txt + "' or ename='" + txt + "' or email='" + txt + "'LIMIT " + display
        print("query 4 =====", query)
    elif commitee != '0' and usertype == '0' and display != '' and txt != '':
        query = "select * from emeet_manageusers where access!='superadmin' and find_in_set(" + commitee + ", committee) and userid = '" + txt + "' or ename = '" + txt + "' or email = '" + txt + "' LIMIT " + display
        print("query 5 =======", query)

    # *******************************************************usertype combination*************************************

    elif commitee == '0' and usertype != '0' and display == '10' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and cmsflag='" + cmsflag + "' LIMIT 20"
        print("query 6 ======", query)

    elif commitee == '0' and usertype != '0' and display != '' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and cmsflag='" + cmsflag + "' LIMIT " + display
        print("query 7 =======", query)
    elif commitee == '0' and usertype != '0' and display != '' and txt != '':
        query = "select * from emeet_manageusers where access!='superadmin' and  cmsflag='" + cmsflag + "' and userid='" + txt + "' or ename='" + txt + "' or email='" + txt + "' LIMIT " + display
        print("query 8 ======", query)

    # *************************************display combination **************************************
    elif commitee == '0' and usertype == '0' and display != '' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and cmsflag='True' or cmsflag='False' LIMIT " + display
        print("query 9 ======", query)
    elif commitee == '0' and usertype == '0' and display != '' and txt != '':
        query = "select * from emeet_manageusers where access!='superadmin' and userid='" + txt + "' or ename='" + txt + "' or email='" + txt + "' LIMIT " + display
        print("query 10 =====", query)
    elif commitee != '0' and usertype == '0' and display != '' and txt == '':
        query = "select * from emeet_manageusers where access!='superadmin' and find_in_set(" + commitee + ",committee)  LIMIT " + display
        print("query 11 ======", query)

    # **************************************************txtbox cobination ******************************
    elif commitee == '0' and usertype == '0' and display == '10' and txt != '':
        query = "select * from emeet_manageusers where access!='superadmin' and userid='" + txt + "' or ename='" + txt + "' or email='" + txt + "' LIMIT 20"
        print("query 12 ======", query)

    cursor.execute(query)
    users = cursor.fetchall()
    print("length============>", len(users))
    # print("\nusers===>", users)

    com_query = EmeetForums.objects.filter(approved='approved',stat__iexact='true').values_list('fid', 'fname')
    cursor = connection.cursor()
    # cursor.execute("select `fid`,`fname` from `emeet_forums` where `approved`='approved' ")
    committee_query = dict(com_query)
    print(committee_query)

    if request.method == "POST":
        userid = request.POST.get('id')
        print("userid: ", userid)

        if userid:

            # com_query = EmeetForums.objects.filter(approved='approved').values_list('fid', 'fname')
            # cursor = connection.cursor()
            # # cursor.execute("select `fid`,`fname` from `emeet_forums` where `approved`='approved' ")
            # committee_query = dict(com_query)
            # print(committee_query)

            cursor.execute("select `committee` from `emeet_manageusers` where `userid`='" + userid + "' ")
            assign_committees = cursor.fetchall()[0][0]
            if assign_committees != None:
                assign_com = assign_committees.split(',')

            else:
                assign_com = []
            print("com: ", assign_com)
            context_data = {'assign_committee': assign_com, 'userid': userid}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            # return redirect(baseURL + 'manageUser',
            #                 {'baseURL': baseURL,'assign_com': assign_com, 'userid': userid})
            # return render(request, 'manageUser.html', {'baseURL': baseURL, 'users': users,'userid':userid,
            #                                        'assign_com':assign_com})

    # -------new change added
    if commitee == None:
        commitee = "0"
    if display == None:
        display = "10"
    if usertype == None:
         usertype = "0"
    if txt == None:
        txt = ""
    cursor.execute("select fname from emeet_forums where fid='"+str(commitee)+"'")
    comname = cursor.fetchall()
    committee_name = "Select Committee"
    if len(comname)>0:
        committee_name = comname[0][0]
    #----------
    query = "select fid,fname from emeet_forums where stat = 'true' or stat = 'True'"
    cursor.execute(query)
    committee_info = cursor.fetchall()

    committee_array = []
    for i in committee_info:
        fid_dict = {"fid": str(i[0])}
        fname_dict = {"fname": i[1]}
        fid_dict.update(fname_dict)
        committee_array.append(fid_dict)

    print(committee_array)

    usertype_arr = []
    utype_list = ['All User Type','CMS User','iPad User']
    j = 0
    for i in utype_list:
        uid_dict = {"uid": str(j)}
        utype_dict = {"utype": i}
        uid_dict.update(utype_dict)
        usertype_arr.append(uid_dict)
        j= j+1
    print("usertype_arr---------->",usertype_arr)

    if usertype == "0":
        utype_name = utype_list[0]
    elif usertype == "1":
        utype_name = utype_list[1]
    elif usertype == "2":
        utype_name = utype_list[2]

    display_list = ['10','20','30','40','50']

    print("usertype------>",utype_name)


    name = "{0}".format(request.session.get('ename'))
    date_time = "{0}".format(request.session.get('date_time'))
    response = name + " " + date_time

    datalength = len(users)
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'manageUser.html', {'baseURL': baseURL, 'users': users, 'committee_list': committee_query,
                                               'committee_array': committee_array, 'response': response,
                                               'length': len(users),'committe_id':commitee,'committee_name':committee_name,'usertype':usertype,'usertype_arr':usertype_arr,'utype_name':utype_name,'display':display,'display_list':display_list,'txt':txt,
                                               'datalength':datalength
                                               })




def addUser(request):
    print("++++++++++++++++++++++++++++++addUser CAlled() +++++++++++++++++++++++++++++++++++++++++++++++++")
    if request.method == 'POST':
        fname = request.POST.get('fname')
        uname = request.POST.get('uname')
        empid = request.POST.get('empid')
        emailid = request.POST.get('emailid')
        mobno = request.POST.get('mobno')
        jd = request.POST.get('jd')
        printr = request.POST.get('print')
        cmsflag = request.POST.get('cmsflag')

        print("fname====>", fname, " | uname===>", uname, " | empid===>", empid, " | emailid===>", emailid,
              "| mobno===>", mobno, " | jd===>", jd, "| printr===>", printr, " | cmsflag===>", cmsflag)

        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=6))
        print("password == ", password)
        # password = strgen.StringGenerator("[\w\d]{10}").render()
        # print("password == ", password)
        pass_wrd = password.encode('utf-8')

        enc_pass = encryption(pass_wrd)
        # print('enc_pass: ',enc_pass)
        enc_passwd = enc_pass.decode('utf-8')
        print(enc_passwd)

        currentdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(currentdate)

        cursor = connection.cursor()
        all = " select * from emeet_manageusers WHERE access!='superadmin' LIMIT 20"
        cursor.execute(all)
        users = cursor.fetchall()

        query = "select * from emeet_manageusers where email='" + emailid + "'"
        count = cursor.execute(query)
        res = cursor.fetchall()
        print("length==", len(res), "count===>", count)

        query1 = "select * from emeet_manageusers where userid='" + uname + "'"
        ucount = cursor.execute(query1)
        res1 = cursor.fetchall()
        print("length==", len(res1), "ucount===>", ucount)

        if count == 0 and ucount == 0:
            print("email/userid does not exist")
            query = "insert into emeet_manageusers(`access`,`active`,`accountStatus`,`ename`,`userid`,`empid`,`email`,`mobile`,`join_dt`,`Print`,`cmsflag`,`pwd`,`pwd_dt`)values('user','true','true','" + fname + "','" + uname + "','" + empid + "','" + emailid + "','" + mobno + "','" + jd + "','" + printr + "','" + cmsflag + "','" + enc_passwd + "','" + str(
                currentdate) + "')"
            print(query)
            cursor.execute(query)
            print("Record Inserted!!!")
            activityLogs(request, "User added: " + uname)

            send_email_user(uname, password, emailid)

            context_data = {'message': 'User added successfully', 'uname': uname}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

        else:
            if count > 0:
                print(res)
                print('Email Id already exists.')
                context_data = {'message': 'Email Id already exists.'}

            else:
                print(res1)
                print('User Name already exists.')
                context_data = {'message': 'User Name already exists.'}

            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time
        return render(request, 'manageUser.html',
                      {'baseURL': baseURL, 'users': users, 'response': response})


def send_email_user(username, password, email):
    try:
        ob = s.SMTP("smtp.gmail.com", 587)
        ob.starttls()
        ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
        subject = "Login Details for Emeeting Application"
        body = "Dear {}, \n\n" \
               "We are pleased to inform that you have been registered as a user for the eMeetings Application being used for conducting its  Executive Committee Meetings on iPads. Please copy the following link on the Safari Browser of your iPad to install the eMeetings Application \n\n" \
               "Link:-[ipad_link]  \n\n" \
               "Once the Application has been installed, you can begin using the said Application for viewing the Agenda of the meetings of the forums of which you are a Member.\n\n" \
               "Please find below the login details:\n\n" \
               "User Name  : '{}' \n\n" \
               "Password  : '{}' \n\n" \
               "For any assistance or clarification, please contact Secretarial Team on 022 XXXXXX / X / X. \n\n" \
               "Warm regards,\n" \
               "Secretarial Team.\n\n" \
               "This is a system generated e-mail, please do not reply to this e-mail.".format(username, username,
                                                                                               password)
        message = "Subject:{}\n\n{}".format(subject, body)
        # reciever = "vedanti@mobitrail.com" #email of person
        ob.sendmail('mobitrail.technology@gmail.com', email, message)
        print("email sent successsfully !!!")
        ob.quit()
    except Exception as e:
        print("Err: ", e)


def viewUser(request):
    print("+++++++++++++++++ViewUSer cAlled++++++++++++++++++++++++++++++")
    if request.method == 'POST':
        userid = request.POST.get('userid')
        print("userid===", userid)
        cursor = connection.cursor()
        query = cursor.execute(
            "select ename,userid,email,empid,mobile,join_dt,Print,cmsflag from emeet_manageusers where userid='" + userid + "'")
        print(query)
        result = cursor.fetchall()
        res = list(result[0])
        print(res)

        li = ['ename', 'userid', 'email', 'empid', 'mobile', 'join_dt', 'printr', 'cmsflag']

        data = {}
        for key in li:
            for value in res:
                data[key] = value
                res.remove(value)
                break

        print("response====>", data)
        return HttpResponse(json.dumps(data, default=str))


def updateUser(request):
    print("++++++++++++++++++++++++++++++updateUser CAlled() +++++++++++++++++++++++++++++++++++++++++++++++++")
    if request.method == 'POST':
        fname = request.POST.get('fname')
        uname = request.POST.get('uname')
        empid = request.POST.get('empid')
        emailid = request.POST.get('emailid')
        mobno = request.POST.get('mobno')
        jd = request.POST.get('jd')
        printr = request.POST.get('print')
        cmsflag = request.POST.get('cmsflag')

        print("fname====>", fname, " | uname===>", uname, " | empid===>", empid, " | emailid===>", emailid,
              "| mobno===>", mobno, " | jd===>", jd, "| printr===>", printr, " | cmsflag===>", cmsflag)

        cursor = connection.cursor()
        query = cursor.execute(
            "update emeet_manageusers set ename='" + fname + "',email='" + emailid + "',empid='" + empid + "',mobile='" + mobno + "',join_dt='" + jd + "',Print='" + printr + "',cmsflag='" + cmsflag + "'  where userid='" + uname + "'")
        print(query)
        activityLogs(request, 'User ' + uname + ' information updated.')
        print("updated successfully !!!")
        return redirect(baseURL + "manageUser")


def downloadUsers(request):
    print("++++++++++++++++++++download USers Data+++++++++++++++++++++++++++++")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Users.csv"'
    q = "SELECT  `userid`,`committee` FROM emeet_manageusers where access!='superadmin'"
    cursor = connection.cursor()
    cursor.execute(q)
    notifications = cursor.fetchall()
    print("notify---->",notifications)
    writer = csv.writer(response)

    query = "select fid,fname from emeet_forums where stat = 'true' or stat = 'True'"
    #query = "select fid,fname from emeet_forums"
    cursor.execute(query)
    committee_info = cursor.fetchall()

    committee_array = ['userid']
    fid_arr = []
    for i in committee_info:
        fid = i[0]
        fid_arr.append(fid)
        fname = i[1]
        committee_array.append(fname)
    print("commitee_array---->", committee_array)
    # writer.writerow(['userid', 'Board Committee', 'Audit Committee', 'HR Committee'])
    writer.writerow(committee_array)

    print("fid_array---------->", fid_arr)
    for data in notifications:

        rows = []
        print(data[0])
        rows.append(data[0])

        if data[1] != None and data[1] != '':
            print("====>>",data[1])
            lst = data[1].split(',')
            print(lst)
            li = []
            for i in range(0,len(lst)):
                li.append(int(lst[i]))


            print("li-----------", li)
            for e in fid_arr:
                if e in li:
                    rows.append('Y')
                else:
                    rows.append('N')
        else:
            for i in range(0, len(fid_arr)):
                rows.append('N')

        print("rows=============\n", rows)
        writer.writerow(rows)

    return response


def removeUser(request):
    print("+++++++++++++++++++++++++++++++++++++removeUser called()+++++++++++++++++++++++++++++++++++++++")
    cursor = connection.cursor()
    removeuserlist = request.POST.getlist('removeUser[]')
    print("removeuserlist===========>", removeuserlist)

    for i in removeuserlist:
        cursor.execute("DELETE FROM `emeet_manageusers` WHERE userid='" + str(i) + "'")
        print("i=====>", str(i))
        activityLogs(request, "User " + str(i) + " has been deleted from User Management.")
    return redirect(baseURL + "manageUser")


def assignCommitteeToUser(request):
    user = request.POST.get('user')
    committee = request.POST.get('committiee')
    print("\n", user, committee, type(committee))

    cursor = connection.cursor()
    if user != None:
        cursor.execute("update `emeet_manageusers` set `committee`='" + str(committee) + "' where `userid`='" + user + "' ")
        print("committee updated")

    return redirect(baseURL + 'manageUser')


def enableUser(request, user):
    # user = request.POST.get('user')
    print("in enableuser \n user: ", user)
    cursor = connection.cursor()
    cursor.execute("select `active` from `emeet_manageusers` where `userid`='" + user + "' ")
    active_status = cursor.fetchone()[0]

    if active_status.lower() == 'true':
        cursor.execute("update `emeet_manageusers` set `active`='False' where `userid`='" + user + "' ")
    elif active_status.lower() == 'false':
        cursor.execute("update `emeet_manageusers` set `active`='True' where `userid`='" + user + "' ")
    print("active status updated")

    return redirect(baseURL + 'manageUser')


def wipeData(request, user):
    # user = request.POST.get('user')
    print("in enableuser \n user: ", user)

    cursor = connection.cursor()
    cursor.execute("update `emeet_manageusers` set `Wipe`=1 where `userid`='" + user + "' ")
    print("wipe status updated")

    return redirect(baseURL + 'manageUser')


def send_email(userid, name, email):
    print("regenerate email=======> ", userid)
    enc_user = encrypt(userid)
    enc_usr = enc_user.decode('utf-8')
    user = urllib.parse.quote(enc_usr)
    try:
        # requote_uri("http://www.sample.com/?id=123 abc")
        # link = "<a href='http://127.0.0.1:8000/resetPassword?i="+enc_usr+"'>Here</a>"
        # print(urllib.parse.urlencode(enc_usr))
        print("=====>", requote_uri(enc_usr))
        print('----------->>> ', urllib.parse.quote(enc_usr))
        link = "<a href=" + resetpass_link + "resetPassword?i=" + user + ">Here</a>"
        print("link:", link)
        ob = s.SMTP("smtp.gmail.com", 587)
        ob.starttls()
        ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
        msg = MIMEMultipart('alternative')
        msg['From'] = 'mobitrail.technology@gmail.com'
        msg['To'] = email
        msg['Subject'] = " Reset Password for Meeting Manager Application"
        html = "Dear " + name + ", <br><br>" \
                                "Please click on the below link to reset your password. <br><br>" \
                                "Click" + link + " to Reset <br><br>" \
                                                 "Regards,<br><br>" \
                                                 "Secretarial Team."
        part1 = MIMEText(html, 'html')
        part2 = MIMEText("Dear " + name + ", \n\n" \
                                          "Please click on the below link to reset your password. \n\n" \
                                          "Click Here to Reset \n\n" \
                                          "Regards,\n\n" \
                                          "Secretarial Team.", 'text')

        # reciever = "vedanti@mobitrail.com" #email of person
        msg.attach(part1)
        msg.attach(part2)
        # print(msg.as_string())

        ob.sendmail('mobitrail.technology@gmail.com', email, msg.as_string())
        print("successsful")
        ob.quit()

    except Exception as e:
        print("Err: ", e)


def regenerateUser(request):
    user = request.POST.get('user')
    email = request.POST.get('email')
    print("\n", user, email)
    cursor = connection.cursor()
    cursor.execute("select `ename`,`email` from `emeet_manageusers` where `userid`='" + user + "' ")
    data = cursor.fetchone()
    user_name = data[0]
    email = data[1]
    print("==========>  ", user, user_name, email)
    send_email(user, user_name, email)
    activityLogs(request, "Password Reset requested for : Bad Data.")
    return redirect(baseURL + 'manageUser')


def resetPassword(request):
    user_i = request.GET.get('i')
    print(len(user_i))
    print(user_i)
    userid = user_i.encode('utf-8')
    print(userid)
    user = decrypt(userid)
    user = user.decode('utf-8')
    print("\n", user)
    return render(request, 'reset_password.html', {'baseURL': baseURL, 'user': user})


def setNewPassword(request):
    user = request.POST.get('user')
    passwd = request.POST.get('password')
    print("set pass:\n", user, passwd)

    pass_wrd = passwd.encode('utf-8')

    enc_pass = encryption(pass_wrd)
    # print('enc_pass: ',enc_pass)
    enc_passwd = enc_pass.decode('utf-8')
    # print(enc_passwd)

    currentdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(currentdate)

    cursor = connection.cursor()
    try:
        cursor.execute("update `emeet_manageusers` set `pwd`='" + enc_passwd + "',`pwd_dt`='" + str(
            currentdate) + "' where `userid`='" + user + "' ")
        print("pass reset!")
    except Exception as e:
        print("expc==> ", e)
    return HttpResponse(baseURL)


########################## Meeting Module (vedanti)#########################################

def downloadMOM(request, id):
    if request.session.has_key('session_key'):

        print("+++++++++++++++++++++++++downloadMOM Called()++++++++++++++++++++++++++")
        print("id===>", id)
        response = HttpResponse(content_type='text/html')
        currentdate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        filename = "MOM_document" + currentdate + ".html"
        print("filename==>", filename)
        response['Content-Disposition'] = 'attachment; filename="' + filename
        cursor = connection.cursor()
        query = "SELECT * FROM `emeet_meeting` where id  ='" + str(id) + "'"
        cursor.execute(query)
        meeting_info = cursor.fetchall()

        title = ''
        venue = ''
        vdate = ''
        print(meeting_info)
        for i in meeting_info:
            vdate = i[1].strftime('%B %Y')
            time = i[1].strftime('%H:%M %p')
            day = i[1].strftime('%d')
            if int(day) < 10:
                day = "0" + day
            venue = i[6]
            title = i[5]

        agenda_response = []

        query = "SELECT ag_id,title,doc,mid,version,aid FROM `emeet_level0` where mid  ='" + str(id) + "' order by aid"
        cursor.execute(query)
        level0 = cursor.fetchall()
        print(level0)
        agendalen = len(level0)
        if agendalen > 0:

            agenda_ag_id = []
            for li in level0:
                agenda_ag_id.append(li[0])

            query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level1` where parent in (" + str(agenda_ag_id).strip(
                '[]') + ") order by aid"
            cursor.execute(query)
            level1 = cursor.fetchall()
            print(level1)
            subagendalen = len(level1)

            subagenda_ag_id = []
            for li in level1:
                subagenda_ag_id.append(li[0])

            query = "SELECT ag_id,title,parent,doc,version,aid FROM `emeet_level2` where parent in (" + str(
                subagenda_ag_id).strip('[]') + ") order by aid"
            cursor.execute(query)
            level2 = cursor.fetchall()
            print(level2)
            subsubagendalen = len(level2)
            print(level0)
            print(level1)
            print(level2)
            subsubagenda_ag_id = []
            for li in level2:
                subsubagenda_ag_id.append(li[0])

            for ag in level0:
                subagendaarr = []

                sss = {}
                ag_title = str(ag[5]) + "." + str(ag[1])
                ag_doc = str(ag[2])

                agenda = {"ag_title": ag_title, "ag_doc": ag_doc, "ag_id": ag[0], "aid": ag[5]}
                sss["agenda"] = agenda

                for sag in level1:
                    if sag[2] == ag[0]:
                        subsubarr = []
                        tmp = getalphaID(sag[5])
                        sag_title = str(ag[5]) + ".(" + tmp + ")" + str(sag[1])
                        sag_doc = str(sag[3])
                        # sub_agenda = {"sag_title": sag_title, "sag_doc": sag_doc}
                        sub_agenda = {"sag_title": sag_title, "sag_doc": sag_doc, "sag_id": sag[0]}

                        subagendaarr.append(sub_agenda)
                        sss["sub_agenda"] = subagendaarr
                        for ssag in level2:
                            if ssag[2] == sag[0]:
                                tmp1 = intToRoman(ssag[5])
                                ssag_title = str(ag[5]) + ".(" + tmp + ")" + "(" + tmp1 + ")" + str(ssag[1])
                                ssag_doc = str(ssag[3])
                                subsubagenda = {"ssag_title": ssag_title, "ssag_doc": ssag_doc}

                                subsubarr.append(subsubagenda)
                                sub_agenda['subsubagenda'] = subsubarr

                agenda_response.append(sss)

        print("agenda =====>", agenda_response, "length----->", len(agenda_response))

        data1 = """
        <html>
        <head>
            <title>MINUTES</title>
        </head>
        <body>
        <div style="text-align:justify;">
        <b><span style="text-transform:uppercase">
                MINUTES OF THE PROCEEDINGS OF THE  """

        data1 += title + """  MEETING OF THE BOARD OF DIRECTORS HELD ON</span>  """
        data1 += day + """th """ + vdate + """ AT <span style="text-transform:uppercase">""" + time + """ AT """ + venue
        data1 += """ </span>  </b>
            </div> <br><br><br>
            <b>
                Time of Commencement: """
        data1 += time + """ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Time of Conclusion:""" + time

        data1 += """    </b><br><br><br>
            <b>Present:	</b>
            <br>  <br><br>
            <b>In attendance:  </b>
            Company Secretary The Chairman extended a warm welcome to the Members at the Meeting.
            <br><br><br>
            <b>Mentioned items:</b><br><br><br><br><br>

            <b>ROUTINE ITEMS:</b><br> """
        agenda_data = "<li style='list-style-type:none;'> "
        agenda_data1 = " </li><br>"
        strin = "<b><ul>"
        for data in agenda_response:
            print("data===>   ", data)
            # agenda_data\
            strin += agenda_data
            for key, value in data.items():
                if key == 'agenda':
                    strin += "<span>"
                    agtitle = value['ag_title']
                    print(agtitle)
                    strin += agtitle + "</span>"
                elif key == 'sub_agenda':
                    for sag in value:
                        strin += "<br><span style='margin-left:30px;'>"
                        sagtitle = sag['sag_title']
                        strin += sagtitle + "</span> "
                        print(sagtitle)

                        if 'subsubagenda' in sag.keys():
                            for ssag in sag['subsubagenda']:
                                strin += "<br><span style='margin-left:60px;'>"
                                ssagtitle = ssag['ssag_title']
                                print(ssagtitle)
                                strin += ssagtitle + "</span>"
                        else:
                            continue
            print("\n")
            strin += agenda_data1
        strin += "</ul></b>"

        print(strin)
        data1 += strin

        data1 += """   <br><br>
            <b>DATE, TIME AND VENUE:</b><br>Meeting ended with vote of thanks to the Chair.<br>The next meeting of the Board would be held on a date, time and venue to be decided by the Chairman.
            <br><br><br>
            <b>PLACE:</b><span style="text-transform:uppercase">""" + venue + """</span>
            <br><br>
            <b>DATE:</b>   <br>
            <br><br>
            <div style="width:200px;float:right;margin:0;"><b> CHAIRMAN</b></div>
            </body>
            </html>"""
        response.write(data1)
        return response
    else:
        return redirect(baseURL)

def notice(request):
    print("++++++++++++++++++++++++++notice called()+++++++++++++++++++++++")
    id = request.POST.get('id')
    print("id---->", id)

    cursor = connection.cursor()
    query = "SELECT * FROM `emeet_meeting` where id  ='" + str(id) + "'"
    cursor.execute(query)
    meeting_info = cursor.fetchall()

    venue = ''
    vdate = ''
    vtime = ''
    print(meeting_info)
    for i in meeting_info:
        vdate = i[1].strftime('%b %d, %Y')
        day = i[1].strftime('%A')
        vtime = i[1].strftime('%H:%M %p')
        venue = i[6]
        fid = i[2]

    query = "SELECT * FROM `emeet_forums` where fid  ='" + str(fid) + "'"
    cursor.execute(query)
    forum_info = cursor.fetchall()

    for f in forum_info:
        fname = f[1]

    print(fname)
    esub = 'Notice for ' + fname + ' Meeting on ' + vdate + ' ' + vtime + ' at ' + venue
    ebody = 'Dear Member,<br><br>We wish to inform that the ' + fname + '  Meeting is scheduled on ' + vdate + ',' + day + ' at ' + vtime + ' at ' + venue + '.<br><br>Regards,<br><br>Secretarial Team.<br><br><br><b>This is a system generated e-mail, please do not reply to this e-mail.</b>'
    data = {'esub': esub, 'ebody': ebody, 'fid': fid}
    print("response====>", data)
    return HttpResponse(json.dumps(data, default=str))


def sendNoticeEmail(request):
    print("+++++++++++++++++sendNoticeEmail() Called++++++++++++++++++++++++++")
    fid = request.POST.get('fid')
    print("fid===>", fid)
    esub = request.POST.get('esub')
    ebody = request.POST.get('ebody')
    esubtextContent = request.POST.get('esubtextContent')
    print("sub==>", esub)
    print('esubtextContent======>', esubtextContent)
    print("ebody==>", ebody)
    cursor = connection.cursor()
    query = "SELECT email FROM `emeet_manageusers` WHERE FIND_IN_SET(" + str(fid) + ", `committee`)"
    cursor.execute(query)

    mailid = cursor.fetchall()
    arr1 = []
    for i in mailid:
        arr1.append(i[0])
    print("arr===>", arr1)
    email = ['ambika@mobitrail.com', 'vedanti@mobitrail.com']
    # send_multiemail(esub, ebody, email)
    send_multiemail(esubtextContent, ebody, email)
    # send_multiemail(esubtextContent, ebody, arr1)
    return redirect(baseURL + 'showcommittee')


def send_multiemail(esub, ebody, email):
    try:
        ob = s.SMTP("smtp.gmail.com", 587)
        ob.starttls()
        ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
        msg = MIMEMultipart('alternative')
        msg['From'] = 'mobitrail.technology@gmail.com'

        msg['To'] = ', '.join(email)
        print("to===>", msg['TO'])
        msg['Subject'] = esub
        # html = "Dear " + name + ", <br><br>" \
        #                         "Please click on the below link to reset your password. <br><br>" \
        #                         "Click" + link + " to Reset <br><br>" \
        #                                          "Regards,<br><br>" \
        #                                          "Secretarial Team."
        html = ebody
        part1 = MIMEText(html, 'html')
        # part2 = MIMEText("Dear " + name + ", \n\n" \
        #                                   "Please click on the below link to reset your password. \n\n" \
        #                                   "Click Here to Reset \n\n" \
        #                                   "Regards,\n\n" \
        #                                   "Secretarial Team.", 'text')

        # reciever = "vedanti@mobitrail.com" #email of person
        msg.attach(part1)
        # msg.attach(part2)
        # print(msg.as_string())

        ob.sendmail('mobitrail.technology@gmail.com', email, msg.as_string())
        print("email sent successsful")
        ob.quit()

    except Exception as e:
        print("Err: ", e)


def uploadMOM(request):
    print("+++++++++++++++uploadMOM Called+++++++++++++++++++++++++++++++++++++++++++++")
    if request.method == "POST":
        myfile_pdf = request.FILES.get('file')
        data = request.POST.get('requestData')
        request_data = json.loads(data)
        id = request_data['mid']

        # id = request.POST.get('mfid')
        # myfile_pdf = request.FILES['filepdf']
        print(myfile_pdf)
        print("id====>", id)

        cursor = connection.cursor()
        query = "SELECT * FROM `emeet_meeting` where id  ='" + str(id) + "'"
        cursor.execute(query)
        meeting_info = cursor.fetchall()

        mid = ''
        fid = ''
        for m in meeting_info:
            mid = m[0]
            fid = m[2]
        print("mid===>", mid, "fid==>", fid)
        #query = "select * from emeet_mom where mid='" + str(mid) + "'" + " and (approved='pending' or approved='approved')"
        query = "select * from emeet_mom where mid='" + str(mid) + "'" + " and fid='"+str(fid)+"' and (approved='pending' or approved='approved')"
        cursor.execute(query)
        res = cursor.fetchall()
        print("len(res)======>", len(res))
        print(res)
        if len(res) > 0:
            context_data = {'message': 'Already a MOM file is Loaded.','flag':'true'}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            #messages.success(request, 'Already a MOM file is Loaded.')
        else:
            #query = "select ag_id from emeet_level0 where mid ='" + str(mid) + "'"
            query = "select ag_id from emeet_level0 where  fid = '"+str(fid)+"' and mid ='" + str(id) + "'"
            cursor.execute(query)
            q = cursor.fetchall()
            print("len(q)=======>", len(q))
            print(q)
            if len(q) == 0:
                context_data = {'message': 'Please add agenda first.','flag':'true'}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
                #messages.success(request, 'Please add agenda first.')
            else:
                fs = FileSystemStorage()
                fname = myfile_pdf.name
                print("fname===", fname)
                currentdate = datetime.datetime.now().strftime("%Y%m%d")
                if (fs.exists(basepath + "/static/resources/" + currentdate + "/" + id + "/" + myfile_pdf.name)):
                    fs.delete(basepath + "/static/resources/" + currentdate + "/" + id + "/" + myfile_pdf.name)
                filename = fs.save(basepath + "/static/resources/" + currentdate + "/" + id + "/" + myfile_pdf.name,
                                   myfile_pdf)

                insert_query = "insert into emeet_mom(`mid`,`pdf`,`fid`,`ver`,`approved`)values('" + mid + "','" + fname + "','" + str(
                    fid) + "','1','pending')"
                cursor.execute(insert_query)
                print("insert_query==>", insert_query)
        return redirect(baseURL + 'info/' + str(id))



def sendEmail(request):
    print('----------------- email api ---------------------')
    mid = request.POST.get('mid')
    type = request.POST.get('type')
    pre_value = request.POST.get('pre_value')
    # print(mid,type,pre_value)

    cursor = connection.cursor()
    cursor.execute(
        "select emeet_meeting.fid,emeet_forums.fname from emeet_meeting INNER JOIN emeet_forums where emeet_meeting.id='" + str(
            mid) + "' " \
                   "and emeet_meeting.fid = emeet_forums.fid")
    forum_query = cursor.fetchone()
    fid = forum_query[0]
    forum = forum_query[1]
    print("forum: ", fid, forum)

    cursor.execute("SELECT email FROM `emeet_manageusers` WHERE committee LIKE '%" + str(
        fid) + "%' and access='user' and (active='true' or active = 'True')")
    email_query = cursor.fetchall()
    # print(email_query)

    email_list = []
    for emails in email_query:
        email_list.append(emails[0])
    print(email_list)

    ob = s.SMTP("smtp.gmail.com", 587)
    ob.starttls()
    ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
    msg = MIMEMultipart('alternative')
    msg['From'] = 'mobitrail.technology@gmail.com'
    msg['To'] = 'vedanti@mobitrail.com'  # replace with email_list

    if type == 'venue':
        from_venue = pre_value
        cursor.execute("select `dt`,`venue` from `emeet_meeting` where id=" + str(mid))
        meeting_data = cursor.fetchone()
        to_venue = meeting_data[1]
        date = datetime.datetime.strptime(str(meeting_data[0]), "%Y-%m-%d  %H:%M:%S")
        date_time = date.strftime("%Y/%m/%d %I:%M%p")
        meet_date = date_time.split(" ")[0]
        meet_time = date_time.split(" ")[1]
        print(from_venue, to_venue, meet_time, meet_date, forum)
        try:
            # ob = s.SMTP("smtp.gmail.com", 587)
            # ob.starttls()
            # ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
            # msg = MIMEMultipart('alternative')
            # msg['From'] = 'mobitrail.technology@gmail.com'
            # msg['To'] = 'vedanti@mobitrail.com'  #replace with email_list

            msg['Subject'] = "Venue Change for " + forum + " Meeting"
            html = "Dear Member,<br/><br/>We wish to inform that the <b><u>venue</u></b> of the '" + forum + "'" \
                                                                                                             " Meeting, scheduled at '" + meet_date + "'  on '" + meet_time + "' ,has been  changed from '" + from_venue + "' to '" + to_venue + "' .<br/><br/> " \
                                                                                                                                                                                                                                                 "We regret the inconvenience caused to you.<br /><br />Regards,<br /><br />Secretarial Team.<br /><br/><br/>" \
                                                                                                                                                                                                                                                 "<b>This is a system generated e-mail, please do not reply to this e-mail.</b> ";
            part1 = MIMEText(html, 'html')
            part2 = MIMEText("Dear Member,We wish to inform that the venue of the '" + forum + "'" \
                                                                                               " Meeting, scheduled at '" + meet_date + "'  on '" + meet_time + "' ,has been  changed from  to . " \
                                                                                                                                                                "We regret the inconvenience caused to you." \
                                                                                                                                                                "Regards, Secretarial Team." \
                                                                                                                                                                "This is a system generated e-mail, please do not reply to this e-mail.",
                             'text')

            msg.attach(part1)
            msg.attach(part2)
            ob.sendmail('mobitrail.technology@gmail.com', ['vedanti@mobitrail.com', 'ambika@mobitrail.com'],
                        msg.as_string())
            print("successsful")
            ob.quit()
        except Exception as e:
            print("Err: ", e)

    elif type == 'date':
        from_date = pre_value
        cursor.execute("select `dt`,`days` from `emeet_meeting` where id=" + str(mid))
        meeting_data = cursor.fetchone()
        days = str(meeting_data[1])
        date = datetime.datetime.strptime(str(meeting_data[0]), "%Y-%m-%d  %H:%M:%S")
        day_name = date.strftime("%A")
        date_time = date.strftime("%Y/%m/%d %I:%M%p")
        to_date = date_time.split(" ")[0]

        print(days, from_date, to_date, forum)
        try:
            msg['Subject'] = "Date Change for " + forum + " Meeting"
            html = "Dear Member,<br/><br/>We wish to inform that the <b><u>date</u></b> of the '" + forum + "'" \
                                                                                                            " Meeting,which was earlier scheduled for <u> '" + from_date + "'  </u> has now been changed to <u> '" + day_name + "' ," \
                                                                                                                                                                                                                                " '" + to_date + "'.</u> The time and venue of the Meeting remain the same.<br/><br/>" \
                                                                                                                                                                                                                                                 "We regret the inconvenience caused to you.<br /><br />Regards,<br /><br />Secretarial Team.<br /><br/><br/>" \
                                                                                                                                                                                                                                                 "<b>This is a system generated e-mail, please do not reply to this e-mail.</b> ";
            part1 = MIMEText(html, 'html')
            part2 = MIMEText("Dear Member,We wish to inform that the date of the '" + forum + "'" \
                                                                                              " Meeting,which was earlier scheduled for  '" + from_date + "' has now been changed to '" + day_name + "' ," \
                                                                                                                                                                                                     "'" + to_date + "',The time and venue of the Meeting remain the same." \
                                                                                                                                                                                                                     "We regret the inconvenience caused to you.Regards,Secretarial Team." \
                                                                                                                                                                                                                     "This is a system generated e-mail, please do not reply to this e-mail.",
                             'text')

            msg.attach(part1)
            msg.attach(part2)
            ob.sendmail('mobitrail.technology@gmail.com', ['vedanti@mobitrail.com'], msg.as_string())
            print("successsful")
            ob.quit()
        except Exception as e:
            print("Err: ", e)

    elif type == 'time':
        from_time = pre_value
        cursor.execute("select `dt`,`days` from `emeet_meeting` where id=" + str(mid))
        meeting_data = cursor.fetchone()
        days = str(meeting_data[1])
        date = datetime.datetime.strptime(str(meeting_data[0]), "%Y-%m-%d  %H:%M:%S")
        day_name = date.strftime("%A")
        date_time = date.strftime("%Y/%m/%d %I:%M%p")
        meet_date = date_time.split(" ")[0]
        to_time = date_time.split(" ")[1]

        print(days, date, from_time, to_time, forum)
        try:
            msg['Subject'] = "Time Change for " + forum + " Meeting"
            html = "Dear Member,<br/><br/>We wish to inform that the <b><u>time</u></b> of the '" + forum + "'" \
                                                                                                            " Meeting, scheduled on '" + day_name + "','" + meet_date + "' has been changed from <u> '" + from_time + "'" \
                                                                                                                                                                                                                      " </u> to <u> '" + to_time + "' .</u> The time and venue of the Meeting remain the same.<br/><br/>" \
                                                                                                                                                                                                                                                   "We regret the inconvenience caused to you.<br /><br />Regards,<br /><br />Secretarial Team.<br /><br/><br/>" \
                                                                                                                                                                                                                                                   "<b>This is a system generated e-mail, please do not reply to this e-mail.</b> ";
            part1 = MIMEText(html, 'html')
            part2 = MIMEText("Dear Member,We wish to inform that the date of the '" + forum + "'" \
                                                                                              " Meeting, scheduled on '" + day_name + "','" + meet_date + "' has been changed from '" + from_time + "'" \
                                                                                                                                                                                                    "  to '" + to_time + "' . The time and venue of the Meeting remain the same." \
                                                                                                                                                                                                                         "We regret the inconvenience caused to you.Regards,Secretarial Team." \
                                                                                                                                                                                                                         "This is a system generated e-mail, please do not reply to this e-mail.",
                             'text')

            msg.attach(part1)
            msg.attach(part2)
            ob.sendmail('mobitrail.technology@gmail.com', ['vedanti@mobitrail.com'], msg.as_string())
            print("successsful")
            ob.quit()
        except Exception as e:
            print("Err: ", e)

    elif type == 'agenda':
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # print(pre_value)
        agenda = ast.literal_eval(pre_value)
        cursor.execute("select `dt`,`days` from `emeet_meeting` where id=" + str(mid))
        meeting_data = cursor.fetchone()
        days = str(meeting_data[1])
        date = datetime.datetime.strptime(str(meeting_data[0]), "%Y-%m-%d  %H:%M:%S")
        day_name = date.strftime("%A")
        date_time = date.strftime("%Y/%m/%d %I:%M%p")
        meet_date = date_time.split(" ")[0]
        meet_time = date_time.split(" ")[1]
        # print("agenda ========> \n",agenda)

        # for data in agenda:
        #     print("data====>>>   ",data)

        agenda_data = "<li style='list-style-type:none;'> "
        agenda_data1 = " </li>"
        strin = "<ul>"
        for data in agenda:
            # print("data===>   ",data)
            # agenda_data\
            strin += agenda_data
            for key, value in data.items():
                if key == 'agenda':
                    strin += "<span>"
                    agtitle = value['ag_title']
                    print(agtitle)
                    strin += agtitle + "</span>"
                elif key == 'sub_agenda':
                    for sag in value:
                        strin += "<br><span style='margin-left:30px;'>"
                        sagtitle = sag['sag_title']
                        strin += sagtitle + "</span> "
                        print(sagtitle)

                        if 'subsubagenda' in sag.keys():
                            for ssag in sag['subsubagenda']:
                                strin += "<br><span style='margin-left:60px;'>"
                                ssagtitle = ssag['ssag_title']
                                print(ssagtitle)
                                strin += ssagtitle + "</span>"
                        else:
                            continue
            print("\n")
            strin += agenda_data1
        strin += "</ul>"

        print(strin)

        print(days, meet_time, meet_date, forum)
        try:
            msg['Subject'] = "Upload of Agenda for " + forum + " Meeting";
            html = "Dear Member,<br/><br/>We are pleased to inform that the Agenda of the '" + forum + "'" \
                                                                                                       " Meeting to be held at <u>'" + meet_time + "'</u> on <u> '" + day_name + "' ,'" + meet_date + "'" \
                                                                                                                                                                                                      " </u> has been uploaded on the eMeetings Application.Following are the agendas of the meeting:<br/><br/> '" + strin + "'<br/><br />Regards,<br /><br />Secretarial Team.<br /><br/><br/>" \
                                                                                                                                                                                                                                                                                                                             "<b>This is a system generated e-mail, please do not reply to this e-mail.</b>";

            part1 = MIMEText(html, 'html')
            part2 = MIMEText("Dear Member,We are pleased to inform that the Agenda of the '" + forum + "'" \
                                                                                                       " Meeting to be held at '" + meet_time + "' on  '" + day_name + "' ,'" + meet_date + "'" \
                                                                                                                                                                                            " has been uploaded on the eMeetings Application.Following are the agendas of the meeting:'" + strin + "' Regards,Secretarial Team." \
                                                                                                                                                                                                                                                                                                   "This is a system generated e-mail, please do not reply to this e-mail. ",
                             'text')

            msg.attach(part1)
            msg.attach(part2)

            ob.sendmail('mobitrail.technology@gmail.com', ['vedanti@mobitrail.com'], msg.as_string())
            print("successsful")
            ob.quit()
        except Exception as e:
            print("Err: ", e)

    elif type == 'minute':
        cursor.execute("select `dt`,`days` from `emeet_meeting` where id=" + str(mid))
        meeting_data = cursor.fetchone()
        days = str(meeting_data[1])
        date = datetime.datetime.strptime(str(meeting_data[0]), "%Y-%m-%d  %H:%M:%S")
        day_name = date.strftime("%A")
        date_time = date.strftime("%Y/%m/%d %I:%M%p")
        meet_date = date_time.split(" ")[0]
        meet_time = date_time.split(" ")[1]

        print(days, meet_time, meet_date, forum)
        try:
            msg['Subject'] = "Upload of Minutes of Meeting for " + forum + " Meeting";
            html = "Dear Member,<br/><br/>We wish to inform that the Minutes of Meeting(MOM) of the '" + forum + "'" \
                                                                                                                 " Meeting to be held at <u>'" + meet_time + "'</u> on <u> '" + day_name + "' ,'" + meet_date + "' </u>" \
                                                                                                                                                                                                                "has been uploaded on the eMeetings Application." \
                                                                                                                                                                                                                "<br /><br />Regards,<br /><br />Secretarial Team.<br /><br/><br/>" \
                                                                                                                                                                                                                "<b>This is a system generated e-mail, please do not reply to this e-mail.</b> ";

            part1 = MIMEText(html, 'html')
            part2 = MIMEText("Dear Member,We wish to inform that the Minutes of Meeting(MOM) of the '" + forum + "'" \
                                                                                                                 " Meeting to be held at '" + meet_time + "' on '" + day_name + "' ,'" + meet_date + "'" \
                                                                                                                                                                                                     "has been uploaded on the eMeetings Application.Regards,Secretarial Team." \
                                                                                                                                                                                                     "This is a system generated e-mail, please do not reply to this e-mail. ",
                             'text')

            msg.attach(part1)
            msg.attach(part2)
            ob.sendmail('mobitrail.technology@gmail.com', ['vedanti@mobitrail.com'], msg.as_string())
            print("successsful")
            ob.quit()
        except Exception as e:
            print("Err: ", e)

    print('\n')
    return redirect(baseURL + 'info/' + str(mid))
    # return render(request,'demo.html',{'agenda':agenda})


def quickUpload(request):
    print("_________________________Quick Upload Called____________________________________")
    file_data = request.FILES.get('file')
    data = request.POST.get('requestData')
    request_data = json.loads(data)
    mid = request_data['mid']
    parent_aid = request_data['aid']
    print('parent_aid  ', parent_aid)
    agenda_type = request_data['type']

    cursor = connection.cursor()
    query = "select emeet_meeting.fid ,emeet_meeting.title, emeet_forums.fname from emeet_meeting INNER JOIN emeet_forums where" \
            " emeet_meeting.id='" + mid + "' and emeet_meeting.fid = emeet_forums.fid "
    print(query)
    cursor.execute(query)
    meeting_data = cursor.fetchall()[0]
    # print(meeting_data)
    fid = meeting_data[0]
    meeting = meeting_data[1]
    committee = meeting_data[2]

    print("mid: ", mid)
    if file_data:
        filename = file_data.name
        print(filename, type(filename))

        fs = FileSystemStorage()

        if (fs.exists(basepath + "static/resources/" + committee + "/" + mid + "/" + mid + "_" + filename)):
            currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = file_data.name
            fname = filename.split('.')[0]
            fext = filename.split('.')[1]
            filename = fname + "_" + currenttime + "." + fext
            print('filename ===> ', filename)
            filename = "lvl" + filename
            fs.save(basepath + "static/resources/" + committee + "/" + mid + "/" + mid + "_" + filename, file_data)
        else:
            file_name = fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + mid + "_" + filename,
                                file_data)

        # a = fs.open(basepath + "static/resources/"+committee+"/"+meeting+"/" + mid + "_" + filename)
        # print("\na ===== ",a)

        zipdata = zipfile.ZipFile(basepath + "static/resources/" + committee + "/" + mid + "/" + mid + "_" + filename)
        zipinfos = zipdata.infolist()
        print("namelist--------->",zipdata.namelist())

        zipfile_extli = []
        for f in zipdata.namelist():
            print('filename -------->',f)
            if not f.lower().endswith('.pdf'):
                print("found invalid file")
                zipfile_extli.append('true')

        if any('true' in ext for ext in zipfile_extli):
           context_data = {'message': 'Only PDF files are allowed.'}
           return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

        ### to unzip uploaded file
        with zipfile.ZipFile(basepath + "static/resources/" + committee + "/" + mid + "/" + mid + "_" + filename,'r') as zip_ref:
            #print("zip_ref--------->",zip_ref)
            zip_ref.extractall(basepath + "static/resources/" + committee + "/" + mid + "/")

        if agenda_type == 'agenda':
            cursor.execute("SELECT MAX(aid) FROM `emeet_level0` WHERE mid=" + str(mid))
            max_angenda_count = cursor.fetchone()[0]
            if max_angenda_count:
                agenda_sr = max_angenda_count + 1
            else:
                agenda_sr = 1
            print("agenda_sr: ", agenda_sr)

            agenda_list = []
            # print("\n zipinfos ==== ",zipinfos)
            for idx, info_data in enumerate(zipinfos):
                agenda_sr = agenda_sr + idx
                agenda_list.append(agenda_sr)
                agendadata = info_data.filename
                agenda_list.append(agendadata)
                agenda_name = agendadata.split('.')[0]
                agenda_list.append(agenda_name)

            print("\n agenda list: ", agenda_list)
            date = '2020-10-13 00:00:00.000'
            insert_query = "insert into `emeet_level0` (`descr`,`fid`,`mid`,`version`,`dt1`,`dt2`,`ColorId`,`aid`,`doc`,`title`) values"
            insert_query1 = "('','" + str(fid) + "','" + str(mid) + "','0','" + date + "','" + date + "','0'"
            i = 0
            while i < len(agenda_list) - 3:
                insert_query += insert_query1 + ", '" + str(agenda_list[i]) + "' ,'" + str(
                    agenda_list[i + 1]) + "' ,'" + str(agenda_list[i + 2]) + "' ),"
                i = i + 3
            insert_query += insert_query1 + ", '" + str(agenda_list[i]) + "' ,'" + str(
                agenda_list[i + 1]) + "' ,'" + str(agenda_list[i + 2]) + "' )"
            print("\nquery=== ", insert_query)

            cursor.execute(insert_query)

        elif agenda_type == 'subagenda':
            print("----------- subagenda ------------")
            cursor.execute("SELECT MAX(aid) FROM `emeet_level1` WHERE parent=" + str(parent_aid))
            max_subangenda_count = cursor.fetchone()[0]
            if max_subangenda_count:
                subagenda_sr = max_subangenda_count + 1
            else:
                subagenda_sr = 1
            print("subagenda_sr: ", subagenda_sr)

            subagenda_list = []
            # print("\n zipinfos ==== ",zipinfos)
            for idx, info_data in enumerate(zipinfos):
                subagenda_sr = subagenda_sr + idx
                subagenda_list.append(subagenda_sr)
                subagendadata = info_data.filename
                subagenda_list.append(subagendadata)
                subagenda_name = subagendadata.split('.')[0]
                subagenda_list.append(subagenda_name)

            print("\n subagenda list: ", subagenda_list)

            insert_query = "insert into `emeet_level1` (`descr`,`version`,`ColorId`,`parent`,`aid`,`doc`,`title`) values"
            insert_query1 = "('','0','0','" + str(parent_aid) + "' "
            i = 0
            while i < len(subagenda_list) - 3:
                insert_query += insert_query1 + ", '" + str(subagenda_list[i]) + "' ,'" + str(
                    subagenda_list[i + 1]) + "' ,'" + str(subagenda_list[i + 2]) + "' ),"
                i = i + 3
            insert_query += insert_query1 + ", '" + str(subagenda_list[i]) + "' ,'" + str(
                subagenda_list[i + 1]) + "' ,'" + str(subagenda_list[i + 2]) + "' )"
            print("\nquery=== ", insert_query)

            cursor.execute(insert_query)

        elif agenda_type == 'sub-subagenda':
            print("-----------sub- subagenda ------------")
            cursor.execute("SELECT MAX(aid) FROM `emeet_level2` WHERE parent=" + str(parent_aid))
            max_subsubangenda_count = cursor.fetchone()[0]
            if max_subsubangenda_count:
                subsubagenda_sr = max_subsubangenda_count + 1
            else:
                subsubagenda_sr = 1
            print("subsubagenda_sr: ", subsubagenda_sr)

            subsubagenda_list = []
            # print("\n zipinfos ==== ",zipinfos)
            for idx, info_data in enumerate(zipinfos):
                subsubagenda_sr = subsubagenda_sr + idx
                subsubagenda_list.append(subsubagenda_sr)
                subsubagendadata = info_data.filename
                subsubagenda_list.append(subsubagendadata)
                subsubagenda_name = subsubagendadata.split('.')[0]
                subsubagenda_list.append(subsubagenda_name)

            print("\n subsubagenda_list list: ", subsubagenda_list)

            insert_query = "insert into `emeet_level2` (`descr`,`version`,`ColorId`,`parent`,`aid`,`doc`,`title`) values"
            insert_query1 = "('','0','0','" + str(parent_aid) + "' "
            i = 0
            while i < len(subsubagenda_list) - 3:
                insert_query += insert_query1 + ", '" + str(subsubagenda_list[i]) + "' ,'" + str(
                    subsubagenda_list[i + 1]) + "' ,'" + str(subsubagenda_list[i + 2]) + "' ),"
                i = i + 3
            insert_query += insert_query1 + ", '" + str(subsubagenda_list[i]) + "' ,'" + str(
                subsubagenda_list[i + 1]) + "' ,'" + str(subsubagenda_list[i + 2]) + "' )"
            print("\nquery=== ", insert_query)

            cursor.execute(insert_query)
            activityLogs(request, "User added sub sub agenda for " + meeting + " of " + committee)

    print("+++++++++++++++++++++++++++++++++++++")
    return redirect(baseURL + 'info/' + str(mid))


def findSubAgendaDetails(request):
    print('\n-------------------------------------')
    mid = request.POST.get('mid')
    agendaType = request.POST.get('type')
    parent_agid = request.POST.get('ag_id')

    print(agendaType, parent_agid)

    cursor = connection.cursor()

    if agendaType == 'subagenda':

        cursor.execute("select title,ag_id from `emeet_level0` where mid = '" + mid + "' ")
        parent_agendatitle = cursor.fetchall()
        parent_aglist = []
        for parent in parent_agendatitle:
            parent_aglist.append(parent)

        parent_agendalist = {}
        parent_agendalist = dict(parent_aglist)
        print("\n", parent_agendalist)

        cursor.execute("select title from `emeet_level0` where ag_id = '" + parent_agid + "' ")
        parent_agenda = cursor.fetchall()[0]

        cursor.execute("SELECT MAX(aid) FROM `emeet_level1` WHERE parent=" + parent_agid)
        subagenda_count = cursor.fetchone()[0]
        if subagenda_count:
            subagenda_count = subagenda_count + 1
        else:
            subagenda_count = 1
        print(subagenda_count)

        subagenda_aid = getalphaID(subagenda_count)
        print(subagenda_aid)

        context_data = {'subagenda_aid': subagenda_aid, 'parent_agendatitle': parent_agendalist,
                        'parent_agenda': parent_agenda,
                        'agendaType': agendaType}
        return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

    elif agendaType == 'sub-subagenda':
        cursor.execute("SELECT MAX(aid) FROM `emeet_level2` WHERE parent=" + parent_agid)
        sub_sub_agenda_count = cursor.fetchone()[0]
        print(sub_sub_agenda_count)
        # if (sub_sub_agenda_count != 'NULL') or (type(sub_sub_agenda_count) != 'NoneType'):
        if sub_sub_agenda_count:
            print("not none")
            sub_sub_agenda_count = sub_sub_agenda_count + 1
        else:
            print("none")
            sub_sub_agenda_count = 1
        print(sub_sub_agenda_count)

        sub_sub_agenda_srno = intToRoman(sub_sub_agenda_count)
        print(sub_sub_agenda_srno)

        context_data = {'sub_sub_agenda_srno': sub_sub_agenda_srno, 'agendaType': agendaType,
                        'parent_agid': parent_agid,
                        'sub_sub_agenda_count': sub_sub_agenda_count}
        return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")


def addSubAgenda(request):
    print("++++++++++++++++++++++++++++++++++++++++++++\n sub add agenda")
    file_data = request.FILES.get('file')
    data = request.POST.get('requestData')
    request_data = json.loads(data)

    mid = request_data['mid']
    agenda_type = request_data['type']
    print(agenda_type)

    cursor = connection.cursor()
    query = "select emeet_meeting.fid ,emeet_meeting.title, emeet_forums.fname from emeet_meeting INNER JOIN emeet_forums where" \
            " emeet_meeting.id='" + mid + "' and emeet_meeting.fid = emeet_forums.fid "
    print(query)
    cursor.execute(query)
    meeting_data = cursor.fetchall()[0]
    print(meeting_data)
    fid = meeting_data[0]
    meeting = meeting_data[1]
    committee = meeting_data[2]

    print(fid, '|', meeting, '|', committee)

    if agenda_type == 'subagenda':
        subagenda_srno = request_data['subagenda_srno']
        sub_srno = getalphaID(subagenda_srno)
        subagenda_title = request_data['subagenda_title']
        subagenda_desc = request_data['subagenda_desc']
        subitem_type = request_data['subitem_type']
        subagenda_parentag = request_data['subagenda_parentag']

        print(mid, ' | ', subagenda_srno, ' | ', subagenda_title, ' | ', subagenda_desc, ' | ', subitem_type, ' | ',
              subagenda_parentag, '\n')

        if file_data:
            filename = file_data.name
            print(filename, type(filename))
            fs = FileSystemStorage()
            if file_data != None:
                # pass
                if (fs.exists(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename)):
                    currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                    filename = file_data.name
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext
                    print('filename ===> ', filename)
                    filename = "lvl1_sb_" + str(sub_srno) + filename
                    fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename,file_data)
                else:
                    file_name = fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename,
                                        file_data)
        else:
            filename = ''

        cursor.execute("insert into `emeet_level1` (`title`,`descr`,`parent`,`doc`,`version`,`aid`,`ColorId`)"
                       "values('" + subagenda_title + "','" + subagenda_desc + "','" + str(
            subagenda_parentag) + "','" + filename + "','0','" + str(sub_srno) + "','0')")
        activityLogs(request, "User added sub agenda for " + meeting + " of " + committee)

    elif agenda_type == 'subag_attachment':
        print('***************** subag_attachment *********************')
        agenda_agid = request_data['agenda_agid']
        sbtitle = request_data['sbtitle']
        sbdesc = request_data['sbdesc']
        sbitemtype = request_data['sbitemtype']

        cursor.execute("SELECT MAX(aid) FROM `emeet_level1` WHERE parent=" + agenda_agid)
        subagenda_count = cursor.fetchone()[0]
        if subagenda_count:
            subagenda_count = subagenda_count + 1
        else:
            subagenda_count = 1
        print(subagenda_count)
        print(mid, ' | ', agenda_agid, ' | ', sbtitle, ' | ', sbdesc, '  | ', subagenda_count, '|', sbitemtype, '\n')

        if file_data:
            filename = file_data.name
            print(filename, type(filename))
            if sbtitle == '':
                sbtitle = filename.split('.')[0]
                str(sbtitle).replace('_', '')
                print("new sbtitle: ", sbtitle)

            fs = FileSystemStorage()
            if file_data != None:
                # pass
                if (fs.exists(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename)):
                    currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                    filename = file_data.name
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext
                    print('filename ===> ', filename)
                    filename = "lvl1_at_" + str(subagenda_count) + filename
                    fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename, file_data)
                else:
                    file_name = fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename,
                                        file_data)
        else:
            filename = ''

        cursor.execute("insert into `emeet_level1` (`title`,`descr`,`parent`,`doc`,`version`,`aid`,`ColorId`)"
                       "values('" + sbtitle + "','" + sbdesc + "','" + str(
            agenda_agid) + "','" + filename + "','0','" + str(subagenda_count) + "','0')")
        activityLogs(request, "User added sub agenda for " + meeting + " of " + committee)

    print("+++++++++++++++++++++++++++++++++++++")
    return redirect(baseURL + 'info/' + str(mid))


def addSubSubAgenda(request):
    print("++++++++++++++++++++++++++++++++++++++++++++\n sub sub add agenda")
    file_data = request.FILES.get('file')
    data = request.POST.get('requestData')
    request_data = json.loads(data)
    agenda_type = request_data['type']
    print(agenda_type)
    # print(request_data,type(request_data))

    mid = request_data['mid']

    cursor = connection.cursor()
    query = "select emeet_meeting.fid ,emeet_meeting.title, emeet_forums.fname from emeet_meeting INNER JOIN emeet_forums where" \
            " emeet_meeting.id='" + mid + "' and emeet_meeting.fid = emeet_forums.fid "
    print(query)
    cursor.execute(query)
    meeting_data = cursor.fetchall()[0]
    print(meeting_data)
    fid = meeting_data[0]
    meeting = meeting_data[1]
    committee = meeting_data[2]

    print(fid, '|', meeting, '|', committee)

    if agenda_type == 'sub-subagenda':
        print('*********** sub_subag ************')
        sub_sub_agenda_srno = request_data['sub_sub_agenda_srno']
        sub_sub_agenda_title = request_data['sub_sub_agenda_title']
        sub_sub_agenda_desc = request_data['sub_sub_agenda_desc']
        sub_sub_item_type = request_data['sub_sub_item_type']
        parent_agid = request_data['parent_agid']
        agenda_count = request_data['agenda_count']

        print(mid, ' | ', parent_agid, '|', sub_sub_agenda_srno, ' | ', sub_sub_agenda_title, ' | ',
              sub_sub_agenda_desc, ' | ', agenda_count, '|',
              sub_sub_item_type, '\n')

        if file_data:
            filename = file_data.name
            print(filename, type(filename))
            fs = FileSystemStorage()
            if file_data != None:
                # pass
                if (fs.exists(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename)):
                    currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                    filename = file_data.name
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext
                    print('filename ===> ', filename)
                    filename = "lvl2_" + agenda_count + filename
                    fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename, file_data)
                else:
                    file_name = fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename,
                                        file_data)
        else:
            filename = ''

        cursor.execute("insert into `emeet_level2` (`title`,`descr`,`parent`,`doc`,`version`,`aid`,`ColorId`)"
                       "values('" + sub_sub_agenda_title + "','" + sub_sub_agenda_desc + "','" + str(
            parent_agid) + "','" + filename + "','0','" + str(agenda_count) + "','0')")
        activityLogs(request, "User added sub sub agenda for " + meeting + " of " + committee)

    elif agenda_type == 'sub_subag_attachment':
        print('*********** sub_subag_attachment ************')
        sub_agenda_agid = request_data['sub_agenda_agid']
        sub_sbtitle = request_data['sub_sbtitle']
        sub_sbdesc = request_data['sub_sbdesc']
        sub_sbitemtype = request_data['sub_sbitemtype']

        cursor.execute("SELECT MAX(aid) FROM `emeet_level2` WHERE parent=" + sub_agenda_agid)
        sub_subagenda_count = cursor.fetchone()[0]
        if sub_subagenda_count:
            sub_subagenda_count = sub_subagenda_count + 1
        else:
            sub_subagenda_count = 1
        print(sub_subagenda_count)
        print(mid, ' | ', sub_agenda_agid, ' | ', sub_sbtitle, ' | ', sub_sbdesc, '  | ', sub_subagenda_count, '|',
              sub_sbitemtype, '\n')

        if file_data:
            filename = file_data.name
            print(filename, type(filename))
            if sub_sbtitle == '':
                sub_sbtitle = filename.split('.')[0]
                str(sub_sbtitle).replace('_', '')
                print("new sbtitle: ", sub_sbtitle)

            fs = FileSystemStorage()
            if file_data != None:
                # pass
                if (fs.exists(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename)):
                    currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                    filename = file_data.name
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext
                    print('filename ===> ', filename)
                    filename = "lvl2_at_" + str(sub_subagenda_count) + filename
                    fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename, file_data)
                else:
                    file_name = fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename,
                                        file_data)
        else:
            filename = ''
        cursor.execute("insert into `emeet_level2` (`title`,`descr`,`parent`,`doc`,`version`,`aid`,`ColorId`)"
                       "values('" + sub_sbtitle + "','" + sub_sbdesc + "','" + str(
            sub_agenda_agid) + "','" + filename + "',"
                                                  "'0','" + str(sub_subagenda_count) + "','0')")
        activityLogs(request, "User added sub sub agenda for " + meeting + " of " + committee)

    print("+++++++++++++++++++++++++++++++++++++")
    return redirect(baseURL + 'info/' + str(mid))


def addAgenda(request):
    print("++++++++++++++++++++++++++++++++++++++++++++\nadd agenda")
    file_data = request.FILES.get('file')
    data = request.POST.get('requestData')
    request_data = json.loads(data)

    print(request_data, type(request_data))

    mid = request_data['mid']
    agenda_srno = request_data['agenda_srno']
    agenda_title = request_data['agenda_title']
    agenda_desc = request_data['agenda_desc']
    item_type = request_data['item_type']

    print(mid, ' | ', agenda_srno, ' | ', agenda_title, ' | ', agenda_desc, ' | ', item_type, '\n')

    cursor = connection.cursor()
    query = "select emeet_meeting.fid ,emeet_meeting.title, emeet_forums.fname from emeet_meeting INNER JOIN emeet_forums where" \
            " emeet_meeting.id='" + mid + "' and emeet_meeting.fid = emeet_forums.fid "
    print(query)
    cursor.execute(query)
    meeting_data = cursor.fetchall()[0]
    print(meeting_data)
    fid = meeting_data[0]
    meeting = meeting_data[1]
    committee = meeting_data[2]

    # cursor.execute("select `fid` from `emeet_meeting` where `id` = '"+mid+"' ")
    # fid = cursor.fetchone()[0]
    print(fid, '|', meeting, '|', committee)

    if file_data:
        filename = file_data.name
        print(filename, type(filename))
        fs = FileSystemStorage()
        if file_data != None:
            # pass
            print("adda agenda===> " + basepath + "/static/resources/" + committee + "/" + mid + "/" + filename)
            if (fs.exists(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename)):
                currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                filename = file_data.name
                fname = filename.split('.')[0]
                fext = filename.split('.')[1]
                filename = fname + "_" + currenttime + "." + fext
                print('filename ===> ', filename)
                filename = "lvl0_" + agenda_srno + filename
                fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename, file_data)
            else:
                file_name = fs.save(basepath + "/static/resources/" + committee + "/" + mid + "/" + filename, file_data)
    else:
        filename = ''
    date = '2020-10-13 00:00:00.000'
    cursor.execute(
        "insert into `emeet_level0` (`title`,`descr`,`fid`,`doc`,`mid`,`version`,`aid`,`dt1`,`dt2`,`ColorId`)"
        "values('" + agenda_title + "','" + agenda_desc + "','" + str(fid) + "','" + filename + "','" + str(
            mid) + "','0','" + agenda_srno + "','" + date + "',"
                                                            "'" + date + "','0')")
    activityLogs(request, "User added agenda for " + meeting + " of " + committee)

    print("+++++++++++++++++++++++++++++++++++++")
    return redirect(baseURL + 'info/' + str(mid))


def updatemeetinginfo(request):
    print('-----------------------------------------------')
    mid = request.POST.get('mid')
    field = request.POST.get('field')
    venue = request.POST.get('to_venue')
    date = request.POST.get('to_date')
    time = request.POST.get('to_time')
    print('-------------  ', mid, field, venue, date, time)

    cursor = connection.cursor()
    cursor.execute("select `dt` from `emeet_meeting` where `id`=" + mid)
    meeting_datetime = cursor.fetchone()[0]
    db_date = datetime.datetime.strptime(str(meeting_datetime), "%Y-%m-%d %H:%M:%S")
    orgmeet_date = str(db_date).split(" ")[0]
    orgmeet_time = str(db_date).split(" ")[1]

    # print(orgmeet_date,orgmeet_time)

    if field == 'venue' and venue != None:
        print(venue)
        cursor.execute("update `emeet_meeting` set `venue`='" + venue + "' where id=" + mid)
    elif field == 'date' and date != None:
        new_date = date + ' ' + orgmeet_time
        print(new_date)
        cursor.execute("update `emeet_meeting` set `dt`='" + new_date + "' where id=" + mid)
    elif field == 'time' and time != None:
        new_time1 = orgmeet_date + ' ' + time
        new_time2 = datetime.datetime.strptime(str(new_time1), "%Y-%m-%d %I:%M%p")
        new_time = new_time2.strftime("%Y-%m-%d %H:%M:%S")
        print(new_time)
        cursor.execute("update `emeet_meeting` set `dt`='" + new_time + "' where id=" + mid)

    print('-------------------------------------------- \n')
    return redirect(baseURL + 'info/' + str(mid))


def calender(request):
    if request.session.has_key('session_key'):
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))

        response = name + " " + date_time
        print(response)

        print("----------- calender -----------")
        cursor = connection.cursor()
        committee = request.GET.get('committee')
        # fid = committee

        print("com-- ", committee, type(committee))
        if committee == '' or committee == None:
            fid = 0
            meetingData = EmeetAnnualMeetings.objects.all().order_by('-id')
        else:
            fid = committee
            meetingData = EmeetAnnualMeetings.objects.filter(fid=committee).order_by('-id')
        print("fid: ", fid)
        print(meetingData)



        cursor.execute("select `fid`,`fname` from `emeet_forums` where `approved` = 'approved' and stat = 'true' or stat = 'True'")
        committee_list = cursor.fetchall()
        committee_data = []
        for committee in committee_list:
            committee_data.append(committee)

        committee_dict = dict(committee_data)
        print('committee_dict==============>> ', committee_dict)

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        datalength = len(meetingData)
        paginator = Paginator(meetingData, 10)
        page = request.GET.get('page')
        meetingData = paginator.get_page(page)

        return render(request, "calender.html",
                      {'response': response, 'committee_dict': committee_dict, 'meetingData': meetingData,
                       'fid': fid, 'response': response, 'datalength': datalength})

    else:
        return redirect(baseURL)


def createCalenderMeeting(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            print("================== craete cal meet ================")
            committee = request.POST.get('committee')
            title = request.POST.get('title')
            date = request.POST.get('date').replace('-', '/')
            time = request.POST.get('time')
            venue = request.POST.get('venue')
            dt = date + " " + time
            db_date = datetime.datetime.strptime(dt, "%Y/%m/%d %I:%M %p").strftime("%d/%m/%Y %I:%M %p")

            cursor = connection.cursor()
            # cursor.execute("select max(id) from `emeet_annual_meetings`")
            # id_count = cursor.fetchone()[0]
            # print(id_count)

            cursor.execute("select `fname` from `emeet_forums` where fid=" + committee)
            forum = cursor.fetchone()[0]
            print("--------------------")
            print(committee, forum, title, dt, venue)
            cursor.execute("INSERT INTO `emeet_annual_meetings`(`forum`, `title`, `dt`, `fid`, `venue`)"
                           " VALUES('" + forum + "','" + title + "','" + db_date + "','" + committee + "','" + venue + "') ")

            activityLogs(request, 'User added calender meeting: ' + title)
            # return redirect(baseURL+'calender',{'committee':committee})
            return HttpResponse(committee)
    else:
        return redirect(baseURL)


def viewCalenderMeeting(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            id = request.POST.get('id')

            cursor = connection.cursor()
            cursor.execute("select * from `emeet_annual_meetings` where id=" + id)
            app_data = cursor.fetchall()
            meetingList = list(app_data[0])

            # meetingData = EmeetAnnualMeetings.objects.filter(id=id)
            # meetingList = list(meetingData)
            print('----------->>> ', meetingList)

            li = ['id', 'forum', 'title', 'dt', 'fid', 'venue', 'company_id']
            meeting_details = {}
            for key in li:
                for data in meetingList:
                    meeting_details[key] = data
                    meetingList.remove(data)
                    break

            print(meeting_details)
            return HttpResponse(json.dumps(meeting_details, default=str))

    else:
        return redirect(baseURL)


def updateCalenderMeeting(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            id = request.POST.get('id')
            title = request.POST.get('title')
            date = request.POST.get('date').replace('-', '/')
            time = request.POST.get('time')
            venue = request.POST.get('venue')
            dt = date + " " + time
            db_date = datetime.datetime.strptime(dt, "%Y/%m/%d %I:%M %p").strftime("%d/%m/%Y %I:%M %p")

            cursor = connection.cursor()
            print("-------------------- update")
            print(id, title, dt, venue)
            cursor.execute(
                "update `emeet_annual_meetings` set `title`='" + title + "', `dt`='" + db_date + "', `venue`='" + venue + "'"
                                                                                                                     " where `id` = '" + id + "' ")
            activityLogs(request, 'User updated calender meeting: ' + title)
            return redirect(baseURL + 'calender')
    else:
        return redirect(baseURL)


def deleteCalenderMeeting(request, id):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM `emeet_annual_meetings` WHERE id=" + str(id))
        print("meeting deleted")
        activityLogs(request, 'User deleted calender meeting')
        messages.success(request,"Calender meeting has been deleted successfully ")
        return redirect(baseURL + 'calender')
    else:
        return redirect(baseURL)


def downloadCalenderMeeting(request, fid):
    print("*********************** download cal ***************************\nfid ====> ", fid)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Calender_Master.csv"'
    cursor = connection.cursor()
    if fid == 0:
        q = "select `forum`,`title`,`dt`,`venue` from `emeet_annual_meetings`"
    else:
        q = "select `forum`,`title`,`dt`,`venue` from `emeet_annual_meetings` where `fid`=" + str(fid)
    cursor.execute(q)
    notifications = cursor.fetchall()
    cursor.close()
    writer = csv.writer(response)
    writer.writerow(['Committee', 'Title', 'Date', 'Venue'])
    for data in notifications:
        print(data)
        committe = data[0]
        title = data[1]
        dt = data[2]
        venue = data[3]
        data = tuple(data)
        writer.writerow([committe, title, dt, venue])
    # name = "{0}".format(request.session.get('ename'))
    # activityLogs(request, "User " + name + " have download activity logs data.")
    return response


def notifications(request):
    if request.session.has_key('session_key'):
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))

        response = name + " " + date_time
        print(response)

        cursor = connection.cursor()
        cursor.execute("select `fid`,`fname` from `emeet_forums` where `approved` = 'approved' ")
        committee_list = cursor.fetchall()
        committee_data = []
        for commdata in committee_list:
            committee_data.append(commdata)

        committee_dict = {0: 'General (Everyone)'}
        committee_dict.update(dict(committee_data))
        print('committee_dict==============>> ', committee_dict)

        notify_list = EmeetMsg.objects.all().order_by('-id')
        # for n in notify_list:
        #     print(n.dt)

        li = []
        #print("cmslogs----->", activities)
        for a in notify_list:
            date_db = (a.dt).strftime("%d/%m/%Y %I:%M %p")
            li.append(date_db)


        datalength = len(notify_list)
        paginator = Paginator(notify_list, 10)
        page = request.GET.get('page')
        notify_list = paginator.get_page(page)
        notify_list1 = zip(notify_list, li)
        return render(request, 'notification.html',
                      {'baseURL': baseURL, 'response': response, 'notify_list': notify_list,'notify_list1': notify_list1,
                       'committee_dict': committee_dict, 'datalength': datalength})
    else:
        return redirect(baseURL)


def createNotification(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            msg = request.POST.get('msg')
            committee = request.POST.get('committee')
            currenttime = datetime.datetime.now()
            cursor = connection.cursor()
            # cursor.execute("select max(id) from `emeet_msg`")
            # id_count = cursor.fetchone()[0]
            # print(id_count)

            query = "insert into `emeet_msg` (`msg`,`dt`,`comm`,`status`) values('" + msg + "','" + str(
                currenttime) + "'," \
                               " '" + committee + "','Active')"
            cursor.execute(query)
            print("notification added")
            activityLogs(request, 'User added notification')
            return redirect(baseURL + 'notifications')
    else:
        return redirect(baseURL)


def deleteNotification(request, id):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM `emeet_msg` WHERE id=" + str(id))
        print("notification deleted")
        activityLogs(request, 'User deleted notification')
        return redirect(baseURL + 'notifications')
    else:
        return redirect(baseURL)


def aboutus(request):
    if request.session.has_key('session_key'):
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))

        response = name + " " + date_time
        print(response)
        print("----------- about us -----------")

        cursor = connection.cursor()

        cursor.execute("select `id`,`name`,`link`,`dt` from `emeet_aboutus` order by `id` desc")
        data_list = cursor.fetchall()

        datalength = len(data_list)
        paginator = Paginator(data_list, 10)
        page = request.GET.get('page')
        data_list = paginator.get_page(page)

        return render(request, 'aboutus.html',
                      {'baseURL': baseURL, 'response': response, 'data_list': data_list, 'pdfurl': pdfurl,
                       'datalength': datalength})
    else:
        return redirect(baseURL)


def uploadDocumentAbtus(request):
    if request.session.has_key('session_key'):
        file_data = request.FILES.get('file')
        data = request.POST.get('requestData')
        request_data = json.loads(data)
        title = request_data['title']
        date = request_data['date']

        if file_data:

            filename = file_data.name

            fs = FileSystemStorage()

            if (fs.exists(basepath + "static/AboutUs/" + filename)):
                currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                fname = filename.split('.')[0]
                fext = filename.split('.')[1]
                filename = fname + "_" + currenttime + "." + fext
                filename1 = pdfurl + filename
                print(filename1)

                fs.save(basepath + "static/AboutUs/" + filename, file_data)
            else:
                filename1 = pdfurl + filename
                file_name = fs.save(basepath + "static/AboutUs/" + filename, file_data)

            cursor = connection.cursor()
            try:
                query = "insert into `emeet_aboutus`(`name`,`link`,`dt`) values('" + title + "','" + filename + "','" + date + "')"
                print(query)
                cursor.execute(query)
                activityLogs(request, 'User added ' + title + ' information')
            except Exception as e:
                print("expect===> ", e)

            return redirect(baseURL + 'aboutus')
    else:
        return redirect(baseURL)


def deleteAboutusDocument(request, id):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM `emeet_aboutus` WHERE id=" + str(id))
        print("document deleted")
        return redirect(baseURL + 'aboutus')
    else:
        return redirect(baseURL)


def viewAboutUs(request):
    if request.session.has_key('session_key'):
        id = request.POST.get('id')
        cursor = connection.cursor()
        cursor.execute("select `id`,`name`,`link`,`dt` from `emeet_aboutus` where `id`=" + id)
        about_usdata = cursor.fetchall()
        about_usList = list(about_usdata[0])

        # meetingData = EmeetAnnualMeetings.objects.filter(id=id)
        # meetingList = list(meetingData)
        print('----------->>> ', about_usList)

        li = ['id', 'title', 'link', 'dt']
        about_us_details = {}
        for key in li:
            for data in about_usList:
                if key == 'link':
                    about_us_details[key] = pdfurl + data
                    about_usList.remove(data)
                else:
                    about_us_details[key] = data
                    about_usList.remove(data)
                break

        print(about_us_details)
        return HttpResponse(json.dumps(about_us_details, default=str))
    else:
        return redirect(baseURL)


def updateAboutUs(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            file_data = request.FILES.get('file')
            data = request.POST.get('requestData')
            request_data = json.loads(data)
            id = request_data['id']
            title = request_data['title']
            date = request_data['date']

            cursor = connection.cursor()
            print("--------------------about us update")
            print(id, title, date)

            if file_data:

                filename = file_data.name
                fs = FileSystemStorage()

                if (fs.exists(basepath + "static/AboutUs/" + filename)):
                    currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext
                    filename1 = pdfurl + filename
                    print(filename1)
                    fs.save(basepath + "static/AboutUs/" + filename, file_data)
                else:
                    filename1 = pdfurl + filename
                    file_name = fs.save(basepath + "static/AboutUs/" + filename, file_data)

                cursor.execute("update `emeet_aboutus` set `name`='" + title + "', `dt`='" + date + "', "
                                                                                                    "`link`='" + filename + "' where `id` = '" + id + "' ")

            else:
                cursor.execute(
                    "update `emeet_aboutus` set `name`='" + title + "', `dt`='" + date + "' where `id` = '" + id + "' ")
            activityLogs(request, 'User updated ' + title + ' information')

            return redirect(baseURL + 'aboutus')
    else:
        return redirect(baseURL)


def errorPage(request):
    return render(request, 'error_page.html')


def sharedDocuments(request):
    if request.session.has_key('session_key'):
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))

        response = name + " " + date_time
        print(response)
        print("----------- shared docs -----------")

        cursor = connection.cursor()
        cursor.execute("select `id`,`name`,`link`,`dt`,`expiryDate` from `emeet_shareddoc` order by `id` desc")
        docs_data = cursor.fetchall()

        cursor.execute("select `userid` from `emeet_manageusers` where `access`='user'")
        userslist = cursor.fetchall()
        users = []
        for usr in userslist:
            users.append(usr[0])
        print("all users: ", users)

        if request.method == "POST":
            id = request.POST.get('id')
            print("post id: ", id)
            if id:
                cursor.execute("select `name` from `emeet_shareddoc` where `id`=" + id)
                title = cursor.fetchone()[0]
                print('title: ', title)

                cursor.execute("select `userid` from `emeet_document_users` where `doc_id`='" + id + "' ")
                assign_users = cursor.fetchall()
                print("====>> ", assign_users)
                assign_userslist = []
                for usr in assign_users:
                    assign_userslist.append(usr[0])
                print(assign_userslist)
                if len(assign_userslist) > 0:
                    assign_user = assign_userslist

                else:
                    assign_user = []
                print("assign user : ", assign_user)
                context_data = {'title': title, 'assign_user': assign_user, 'id': id}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")

        datalength = len(docs_data)
        paginator = Paginator(docs_data, 10)
        page = request.GET.get('page')
        docs_data = paginator.get_page(page)

        return render(request, 'shared_docs.html',
                      {'baseURL': baseURL, 'response': response, 'docs_data': docs_data, 'users': users,
                       'datalength': datalength})
    else:
        return redirect(baseURL)


def addSharedDocs(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            file_data = request.FILES.get('file')
            data = request.POST.get('requestData')
            request_data = json.loads(data)
            title = request_data['title']
            startdate = request_data['start_date']
            expirydate = request_data['expiry_date']

            cursor = connection.cursor()
            print("-------------------- add share doc")
            print(title, startdate, expirydate)

            if file_data:
                currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                filename = file_data.name

                fs = FileSystemStorage()

                if (fs.exists(basepath + "static/SharedDocs/1/" + filename)):
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext

                    fs.save(basepath + "static/SharedDocs/1/" + filename, file_data)
                else:
                    file_name = fs.save(basepath + "static/SharedDocs/1/" + filename, file_data)

                cursor.execute("insert into `emeet_shareddoc` (`name`,`link`,`dt`,`company`,`expiryDate`) "
                               "values('" + title + "','" + filename + "','" + startdate + "','1','" + expirydate + "') ")

                print("shared doc added")

            return redirect(baseURL + 'sharedDocs')
    else:
        return redirect(baseURL)


def viewSharedDocs(request):
    if request.session.has_key('session_key'):
        id = request.POST.get('id')
        cursor = connection.cursor()
        cursor.execute("select `id`,`name`,`dt`,`expiryDate` from `emeet_shareddoc` where `id`=" + id)
        docs_data = cursor.fetchall()
        docs_List = list(docs_data[0])

        # meetingData = EmeetAnnualMeetings.objects.filter(id=id)
        # meetingList = list(meetingData)
        print('----------->>> ', docs_List)

        li = ['id', 'title', 'dt', 'expiryDate']
        docs_details = {}
        for key in li:
            for data in docs_List:
                docs_details[key] = data
                docs_List.remove(data)
                break

        print(docs_details)
        return HttpResponse(json.dumps(docs_details, default=str))
    else:
        return redirect(baseURL)


def updateSharedDocs(request):
    if request.session.has_key('session_key'):
        if request.method == 'POST':
            file_data = request.FILES.get('file')
            data = request.POST.get('requestData')
            request_data = json.loads(data)
            id = request_data['id']
            title = request_data['title']
            startdate = request_data['startdate']
            expirydate = request_data['expirydate']

            cursor = connection.cursor()
            print("--------------------  shared docs update")
            print(id, title, startdate, expirydate)

            if file_data:
                currenttime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                filename = file_data.name

                fs = FileSystemStorage()

                if (fs.exists(basepath + "static/SharedDocs/1/" + filename)):
                    fname = filename.split('.')[0]
                    fext = filename.split('.')[1]
                    filename = fname + "_" + currenttime + "." + fext
                    fs.save(basepath + "static/SharedDocs/1/" + filename, file_data)
                else:
                    file_name = fs.save(basepath + "static/SharedDocs/1/" + filename, file_data)

                cursor.execute("update `emeet_shareddoc` set `name`='" + title + "', `dt`='" + startdate + "', "
                                                                                                           "`link`='" + filename + "',`expiryDate`='" + expirydate + "' where `id` = '" + id + "' ")

            else:
                cursor.execute("update `emeet_shareddoc` set `name`='" + title + "', `dt`='" + startdate + "', "
                                                                                                           " `expiryDate`='" + expirydate + "' where `id` = '" + id + "' ")

            return redirect(baseURL + 'sharedDocs')
    else:
        return redirect(baseURL)


def deleteSharedDocs(request, id):
    if request.session.has_key('session_key'):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM `emeet_shareddoc` WHERE id=" + str(id))
        print("share document deleted")
        return redirect(baseURL + 'sharedDocs')
    else:
        return redirect(baseURL)


def assignSharedDocsUser(request):
    print("------------------- assign shared docsusr ------------------")
    id = request.POST.get('id')
    users = request.POST.get('users')
    userlist = users.split(',')
    print("\nuserlist----> ", id, userlist)
    currentdate = datetime.datetime.now()
    cursor = connection.cursor()

    cursor.execute("select `userid` from `emeet_document_users` where `doc_id`=" + id)
    doc_users = cursor.fetchall()
    # print("doc usrs: ",doc_users)
    doc_userslist = []
    for duser in doc_users:
        doc_userslist.append(duser[0])
    # if duser not in userlist:
    # cursor.execute("delete from `emeet_document_users` where userid='"+ duser[0] +"' and `doc_id`='"+ id +"' ")
    # print(duser[0]," doc user deleted")
    #     doc_userslist.append(duser)
    print('doc user list----->> ', doc_userslist)

    # for user in userlist:
    #     cursor.execute("select `userid` from `emeet_document_users` where `userid`='" + user + "' and `doc_id`='"+ id +"'  ")
    #     dbuser = cursor.fetchall()
    #     print("dbuser: ",dbuser)
    #     #if len(isuser) == 0:
    #     if len(dbuser)>0:
    #         pass
    #         #cursor.execute("update `emeet_document_users` set`dt`='"+str(currentdate)+"' where `userid`='"+user+"' and `doc_id`='"+id+"'")
    #     else:
    #         #cursor.execute("insert into `emeet_document_users` (`userid`,`doc_id`,`dt`) values('"+user+"','"+id+"','"+str(currentdate)+"')")
    #         print(user," doc user added")

    for user in userlist:
        print('user-----> ', user)
        for duser in doc_userslist:
            print('dc user-----> ', duser)
            if duser in userlist and user in doc_userslist:
                # pass
                print("user is in db and new list")
            elif duser not in userlist:
                cursor.execute(
                    "delete from `emeet_document_users` where userid='" + duser + "' and `doc_id`='" + id + "' ")
                print("user is in db but not in new list")
                doc_userslist.remove(duser)
                print('doc_userslist: ', doc_userslist)

        if user not in doc_userslist:
            cursor.execute(
                "insert into `emeet_document_users` (`userid`,`doc_id`,`dt`) values('" + user + "','" + id + "','" + str(
                    currentdate) + "')")
            print("user not in db but in new list")

    return redirect(baseURL + 'sharedDocs')


# +++++++++++++++++++++Directos (Ambika) +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def showDirectors(request):
    if request.session.has_key('session_key'):
        print("++++++++++++++++showDirectors Called()++++++++++++++++++++++++++++")
        member = EmeetBoardMembers.objects.all()
        print(member)
        print("length===>", len(member))
        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time

        datalength = len(member)
        paginator = Paginator(member, 10)
        page = request.GET.get('page')
        member = paginator.get_page(page)
        return render(request, "directors.html",
                      {'baseURL': baseURL, 'member': member, 'response': response, 'datalength': datalength})
    else:
        return redirect(baseURL)


def addMember(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++++++addMember Called() ++++++++++++++++++++++++++++++++")
        if request.method == "POST":
            img = request.FILES.get('img')
            data = request.POST.get('requestData')
            request_data = json.loads(data)
            id = request_data['id']
            dob = request_data['dob']
            edu = request_data['education']
            desg = request_data['desg']
            name = request_data['name']
            achv = request_data['achv']
            fname = ''

            print("id===>", id, " | dob===>", dob, " | edu===>", edu, " | desg===>", desg, "| naem===> ", name,
                  "| achv====>", achv)
            if img != None:
                fs = FileSystemStorage()
                fname = img.name
                print("fname===", fname)

                if (fs.exists(basepath + "/static/resources/Board Members/" + img.name)):
                    fs.delete(basepath + "/static/resources/Board Members/" + img.name)
                filename = fs.save(basepath + "/static/resources/Board Members/"  + img.name,
                                   img)
            member = EmeetBoardMembers.objects.all()

            print("length===>", len(member))
            sr = len(member) + 1

            cursor = connection.cursor()
            query = "select * from emeet_board_members where id='" + str(id) + "'"
            count = cursor.execute(query)
            res = cursor.fetchall()
            print("length==", len(res), "count===>", count)
            if count == 0:
                print("id does not exist")
                add = EmeetBoardMembers(id=id, name=name, desg=desg, detail=achv, image=fname, dob=dob, qualify=edu,
                                        srno=sr)
                add.save()
                print(add)
                print("inserted !!!")
                activityLogs(request, "Board Member Added : " + name)
                context_data = {'message': 'Member added successfully .'}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            else:
                print(res)
                context_data = {'message': 'ID already exists.'}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            return redirect(baseURL + 'showDirectors')
    else:
        return redirect(baseURL)


def viewMember(request):
    if request.session.has_key('session_key'):
        print("++++++++++++++++++viewMember Called()++++++++++++++++++++++++")
        if request.method == 'POST':
            id = request.POST.get('id')
            name = request.POST.get('name')
            print("id===", id, "name===>", name)
            cursor = connection.cursor()
            query = cursor.execute(
                "select id,name,desg,detail,image,srno,dob,qualify from emeet_board_members where id='" + str(id) + "'")
            print(query)
            result = cursor.fetchall()
            res = list(result[0])
            print(res)

            li = ['id', 'name', 'desg', 'detail', 'image', 'srno', 'dob', 'qualify']

            data = {}
            for key in li:
                for value in res:
                    data[key] = value
                    res.remove(value)
                    break

            print("response====>", data)
            activityLogs(request, "User Viewed Board Member for " + name)
            return HttpResponse(json.dumps(data, default=str))
    else:
        return redirect(baseURL)


def updateMember(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++++++updateMember Called() ++++++++++++++++++++++++++++++++")
        if request.method == "POST":
            img = request.FILES.get('img')
            data = request.POST.get('requestData')
            request_data = json.loads(data)
            cid = request_data['cid']
            id = request_data['id']
            dob = request_data['dob']
            edu = request_data['education']
            desg = request_data['desg']
            name = request_data['name']
            achv = request_data['achv']
            fname = ''

            print("cid=====>", cid)
            print("id===>", id, " | dob===>", dob, " | edu===>", edu, " | desg===>", desg, "| naem===> ", name,
                  "| achv====>", achv)
            if img != None:
                fs = FileSystemStorage()
                fname = img.name
                print("fname===", fname)

                if (fs.exists(basepath + "/static/resources/Board Members/" + img.name)):
                    fs.delete(basepath + "/static/resources/Board Members/" + img.name)
                filename = fs.save(basepath + "/static/resources/Board Members/" + img.name,
                                   img)


            cursor = connection.cursor()
            query = "select * from emeet_board_members where id='" + str(id) + "'"
            count = cursor.execute(query)
            res = cursor.fetchall()
            print("length==", len(res), "count===>", count)
            if count == 0 or cid == id:
                print("id does not exist")
                if fname != '':
                    update = EmeetBoardMembers.objects.filter(id=cid).update(id=id, name=name, desg=desg, detail=achv,
                                                                         image=fname, dob=dob, qualify=edu)
                else:
                    update = EmeetBoardMembers.objects.filter(id=cid).update(id=id, name=name, desg=desg, detail=achv,
                                                                              dob=dob, qualify=edu)
                print(update)
                print("user updated successfully !!!!")
                activityLogs(request, "Board Member Updated : " + name)
                context_data = {'message': 'Member updated successfully .'}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            else:
                print(res)
                context_data = {'message': 'ID already exists.'}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            return redirect(baseURL + 'showDirectors')
    else:
        return redirect(baseURL)


def deleteMember(request, id, name):
    if request.session.has_key('session_key'):
        print("++++++++++++++deleteMEmber() +++++++++++++++++++++++++")
        print("id---------->", id)
        d = EmeetBoardMembers.objects.get(id=id)
        d.delete()
        print("record deleted successfully !!!")
        activityLogs(request, "Board Member Deleted : " + name)
        return redirect(baseURL + 'showDirectors')
    else:
        return redirect(baseURL)


def downloadAttendanceReport(request, fid):
    cursor = connection.cursor()
    committee = request.GET.get('committee')

    cursor.execute('select `fname` from `emeet_forums` where fid=' + str(fid))
    forum = cursor.fetchone()[0]
    print('forum-------> ', forum)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + forum + '.csv'

    query = "SELECT `userid`,`ename` from `emeet_manageusers` WHERE committee like '%" + str(
        fid) + "%' and `access`='user' "
    cursor.execute(query)
    users = cursor.fetchall()
    print("users =========> ", users)

    # for usr in users:
    #     cursor.execute("select `mid`,`userid`,`status` from `emeet_attend` where `fid` = '"+committee+"'and `remarks`='Marked' "
    #       "and `userid` = '"+usr+"' ")

    cursor.execute("select `title`,`dt`,`id` from `emeet_meeting` where fid = " + str(fid))
    meetings = cursor.fetchall()
    print("meetings =======> ", meetings)

    print(cursor.execute(
        "select `mid`,`userid`,`status` from `emeet_attend` where `fid` = '" + str(fid) + "'and `remarks`='Marked' "))
    marked_users = cursor.fetchall()

    print('marked_users ====>> ', marked_users)

    att = []
    for aele in marked_users:
        att.append(aele[0])
    tbl = []
    for usr in users:
        entry = []
        entry.append(usr[0])
        entry.append(usr[1])
        for meet in meetings:
            for mkdu in marked_users:

                print(mkdu[0], meet[2], usr[0], mkdu[1])
                if str(mkdu[0]) == str(meet[2]) and usr[0] == mkdu[1]:
                    print("inside")
                    if mkdu[2] == 'true':
                        entry.append('Present')
                    elif mkdu[2] == 'false':
                        entry.append('Absent')

                    break
            else:

                if str(meet[2]) in att:
                    print("infalse")
                    # entry.append('false')
                    entry.append("Not Marked")
                else:
                    # entry.append("disabled")
                    entry.append("Not Marked")
        tbl.append(entry)
        print(entry)
    print(tbl)

    cursor.close()
    writer = csv.writer(response)
    field_list = ['UserId', 'User']
    for idx, meet in enumerate(meetings):
        meeting = str(idx + 1) + '.' + meet[0] + ' [' + (meet[1]).strftime("%d/%m/%Y %I:%M:%S %p") + ']'
        print(meeting)
        field_list.append(meeting)

    writer.writerow(field_list)

    for field in field_list:
        for data in tbl:
            # data = list(data)
            print(data)
            # field = data[0]
            #
            # # print(list(users))
            # data.remove(data[0])
            writer.writerow(data)
        break
        #     list(users).remove(data[0])
        # field_list.remove(field)

        # dt = data[2]
        # venue = data[3]
        # data = tuple(data)
        # writer.writerow([field])
    # name = "{0}".format(request.session.get('ename'))
    # activityLogs(request, "User " + name + " have download activity logs data.")
    return response


################################### ambika new ########################################
# ++++++++++++++++++++++++++++++++++++++++++Voting Resolution+++++++++++++++++++++++++++++++++++++++++++++
def showVotingResolution(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++++showVotingResolution Called()+++++++++++++++")
        approval = EmeetApprovals.objects.all().order_by('-expiry_dt')
        print(approval)

        cursor = connection.cursor()

        cursor.execute("select company from emeet_approvals order by expiry_dt desc")
        comit = cursor.fetchall()
        print(comit)

        li = []
        for i in comit:
            cursor.execute("select fname from emeet_forums where fid=" + str(i[0]))
            forum = cursor.fetchone()
            li.append(forum[0])
        print(li)

        appr = zip(approval, li)

        query = "select fid,fname from emeet_forums where stat = 'true' or stat = 'True'"
        cursor.execute(query)
        committee_info = cursor.fetchall()

        committee_array = []
        for i in committee_info:
            fid_dict = {"fid": i[0]}
            fname_dict = {"fname": i[1]}
            fid_dict.update(fname_dict)
            committee_array.append(fid_dict)

        print(committee_array)

        datalength = len(approval)
        paginator = Paginator(approval, 10)
        page = request.GET.get('page')
        approval = paginator.get_page(page)

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time
        return render(request, 'votingResolution.html',
                      {'baseURL': baseURL, 'approval': approval, 'committee_array': committee_array, 'appr': appr,
                       'basepath': basepath, 'response': response, 'datalength': datalength})
    else:
        return redirect(baseURL)


def addVR(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++++++++++++AddVR Called()+++++++++++++++++++++++++++++++")
        if request.method == 'POST':
            file = request.FILES.get('file')

            data = request.POST.get('requestData')
            request_data = json.loads(data)
            title = request_data['title']
            ex_date = request_data['ex_date']
            committee = request_data['committee']
            userlist = request_data['selected']

            fname = ''
            print("title====>", title, " | ex_date====>", ex_date, " | committee====>", committee)
            print("file ====>", file)
            print("userlist====>", userlist)
            q = EmeetApprovals.objects.all()
            id = len(q) + 1

            if file != None:
                fs = FileSystemStorage()
                fname = file.name
                print("fname===", fname)

                if (fs.exists(basepath + "/static/approvals/" + committee + "/" + file.name)):
                    fs.delete(basepath + "/static/approvals/" + committee + "/" + file.name)
                filename = fs.save(basepath + "/static/approvals/" + committee + "/" + file.name,
                                   file)

            add = EmeetApprovals(id=id, title=title, filename=fname, company=committee, expiry_dt=ex_date)
            add.save()
            print("added !!!!!!!")

            for i in userlist:
                # ap = EmeetApprovalUsers(id=id,userid=str(i),action='Pending',mailsent='1')
                # ap.save()
                print("i=====>", str(i))
                cursor = connection.cursor()
                query = "insert into `emeet_approval_users` (`id`,`userid`,`action`,`mailsent`) values('" + str(
                    id) + "','" + str(i) + "','Pending', '1')"
                print(query)
                cursor.execute(query)
            print("user added")
            activityLogs(request,
                         "Voting Resolution Added : PDF document " + fname + " Uploaded for " + str(id) + " " + title)

            return redirect(baseURL + 'showVotingResolution')
    else:
        return redirect(baseURL)


def viewVR(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++viewVR Called()+++++++++++++++++++++")
        if request.method == 'POST':
            id = request.POST.get('id')
            title = request.POST.get('title')
            print('id====>', id, "  | title===>", title)

            cursor = connection.cursor()
            cursor.execute("select expiry_dt from emeet_approvals where id =" + str(id))
            res = cursor.fetchall()
            print(res)

            data = {'expiry': res[0]}
            print("response===>", data)
            return HttpResponse(json.dumps(data, default=str))
    else:
        return redirect(baseURL)


def updateVR(request):
    if request.session.has_key('session_key'):
        print("++++++++++++++++++updateVR() Called+++++++++++++++++++++++++++++++++")
        if request.method == 'POST':
            id = request.POST.get('id')
            title = request.POST.get('title')
            expiry = request.POST.get('expiry')

            print("id===>", id, " | title ===>", title, " | expiry===>", expiry)
            update = EmeetApprovals.objects.filter(id=id).update(expiry_dt=expiry)
            print("expiry date  updated successfully !!!!")
            activityLogs(request, "Voting Resolution Updated : " + title)
            return redirect(baseURL + 'showVotingResolution')
    else:
        return redirect(baseURL)


def deleteVR(request, id, filename):
    # def deleteVR(request):
    if request.session.has_key('session_key'):
        print("++++++++++++++deleteMEmber() +++++++++++++++++++++++++")
        # if request.method == 'POST':
        #     id = request.POST.get('id')
        #     filename=request.POST.get('filename')
        print("id---------->", id)
        print("filename==>", filename)
        d = EmeetApprovals.objects.get(id=id)
        d.delete()
        print("record deleted successfully !!!")
        approval_user = EmeetApprovalUsers.objects.filter(id=id).delete()
        print("deleted users")
        activityLogs(request, "PDF document " + filename + " Deleted")
        messages.success(request, "Document Deleted successfully")
        return redirect(baseURL + 'showVotingResolution')
    else:
        return redirect(baseURL)


def getUser(request):
    if request.session.has_key('session_key'):
        print("++++++++++getUSer()++++++++++++++")
        if request.method == 'POST':
            commitee = request.POST.get('fid')
            print("fid=====>", commitee)

            cursor = connection.cursor()
            cursor.execute("select userid from emeet_manageusers where find_in_set(" + commitee + ",committee)  ")
            userid = cursor.fetchall()
            print(userid)
            li = []
            for i in userid:
                li.append(i[0])
            print("li=====>", li)
            data = {'userid': li}
            print("dat==>", data)
            return HttpResponse(json.dumps(data, default=str))
    else:
        return redirect(baseURL)


def viewassignVR(request):
    if request.session.has_key('session_key'):
        print("++++++++++getUSer()++++++++++++++")
        if request.method == 'POST':
            commitee = request.POST.get('fid')
            id = request.POST.get('id')
            print("fid=====>", commitee, "| id========>", id)

            cursor = connection.cursor()
            cursor.execute("select userid from emeet_manageusers where find_in_set(" + commitee + ",committee)  ")
            userid = cursor.fetchall()
            print(userid)
            li = []
            for i in userid:
                li.append(i[0])
            print("li=====>", li)

            cursor.execute("select userid from emeet_approval_users where id= " + str(id))
            chkusers = cursor.fetchall()
            print(chkusers)
            li1 = []
            for i in chkusers:
                li1.append(i[0])
            print("li1=====>", li1)

            data = {'userid': li, 'chkusers': li1}
            print("dat==>", data)
            return HttpResponse(json.dumps(data, default=str))
    else:
        return redirect(baseURL)


def assignVR(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++AssignVR() Called()+++++++++++++++++++++++++")
        if request.method == 'POST':
            id = request.POST.get('id')
            selected = request.POST.getlist('selected[]')
            print("id=====>", id, "selected====>", selected)

            cursor = connection.cursor()
            cursor.execute("select * from emeet_approval_users where id= " + str(id))
            chkusers = cursor.fetchall()
            print(chkusers)
            li1 = []
            for i in chkusers:
                li1.append(i[1])
            print("li1=====>", li1)

            for a in selected:
                if a not in li1:
                    print("new elem checked==>", a)
                    cursor = connection.cursor()
                    query = "insert into `emeet_approval_users` (`id`,`userid`,`action`,`mailsent`) values('" + str(
                        id) + "','" + str(a) + "','Pending', '1')"
                    print(query)
                    cursor.execute(query)
                    print("added")

            for b in li1:
                if b not in selected:
                    print("existing elem unchecked===>", b)
                    cursor = connection.cursor()
                    query = "delete from emeet_approval_users where id='" + str(id) + "' and userid='" + str(b) + "'"
                    print(query)
                    cursor.execute(query)
                    print("deleted")
            return redirect(baseURL + 'showVotingResolution')
    else:
        return redirect(baseURL)


def viewActionsVR(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++viewActionsVR called()++++++++++++++++++++++++")
        if request.method == 'POST':
            id = request.POST.get('id')
            print("id=====>", id)

            cursor = connection.cursor()
            cursor.execute("select userid,action,comments,dt from emeet_approval_users where id=" + str(id))
            res = cursor.fetchall()
            print(res)

            li = []
            for i in res:
                li.append(i[0])
                li.append(i[1])
                if i[2] == None:
                    li.append("")
                else:
                    li.append(i[2])
                if i[3] == None:
                    li.append("")
                else:
                    li.append(i[3].strftime('%d/%m/%Y %H:%M %p'))

            data = {'data': li}
            print("data=========>", data)
            return HttpResponse(json.dumps(data, default=str))
    else:
        return redirect(baseURL)


# ================================================Audit Trails +++++++++++++++++++++++++++++++++
def showAudit(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++++++showAudit calleD()+++++++++++++++++++++++++++++")

        sdate = request.GET.get('sd')
        edate = request.GET.get('ed')

        userid = request.GET.get('user')
        print("userid===>", userid)
        print("sd====>", sdate, " | ed====>", edate)

        cursor = connection.cursor()
        cursor.execute("select userid,ename from emeet_manageusers where access='user'")
        user = cursor.fetchall()
        # print(user)
        ulist = []

        cursor.execute("select count(userid) from emeet_manageusers where access='user'")
        tuser = cursor.fetchall()
        for i in tuser:
            total_user = i[0]

        for i in user:
            uid_dict = {"uid": i[0]}
            ename_dict = {"ename": i[1]}
            uid_dict.update(ename_dict)
            ulist.append(uid_dict)

        print("userlist======>", ulist)
        print("total user===>", total_user)

        eventDetails = []
        tu_dict = {'eventName': 'Total_User', 'count': total_user}
        eventDetails.append(tu_dict)

        li = ['Login_Success', 'Login_Failed', 'Meeting_Document_Accessed', 'Total_Mails_Sent',
              'Documents_Notes_created']
        if sdate is None and edate is None:
            data = [total_user]
            for i in li:
                q = "select EventName,count(EventName) as count from activity_logs_modules where EventName in('" + str(
                    i) + "')  group by EventName order by EventName"
                # print(q)
                cursor.execute(q)
                res = cursor.fetchall()
                # print("length====>",len(res)," ====>",res)

                if len(res) == 0:
                    evname = {'eventName': str(i), 'count': 0}
                    eventDetails.append(evname)
                    data.append(0)
                else:
                    for e in res:
                        evname = {'eventName': e[0]}
                        count = {'count': e[1]}
                        evname.update(count)
                        eventDetails.append(evname)
                        data.append(e[1])

        else:
            data = [total_user]

            for i in li:
                # select EventName,count(EventName) as count from activity_logs_modules where EventName in('Login_Success') and cast(Date as Date) between '2020-10-09' and '2020-10-14'  group by EventName order by EventName
                q = "select EventName,count(EventName) as count from activity_logs_modules where EventName in('" + str(
                    i) + "') and cast(Date as Date) between '" + sdate + "' and '" + edate + "'  group by EventName order by EventName"
                print(q)
                cursor.execute(q)
                res = cursor.fetchall()
                # print(res)

                if len(res) == 0:
                    evname = {'eventName': str(i), 'count': 0}
                    eventDetails.append(evname)
                    data.append(0)
                else:
                    for e in res:
                        evname = {'eventName': e[0]}
                        count = {'count': e[1]}
                        evname.update(count)
                        eventDetails.append(evname)
                        data.append(e[1])
            print("data====>", data)
            context_data = {'data': data}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
        if userid != None:
            data = [total_user]
            for i in li:
                q = "select EventName,count(EventName) as count from activity_logs_modules where EventName in('" + str(
                    i) + "') and userid='" + str(userid) + "' group by EventName order by EventName"
                print(q)
                cursor.execute(q)
                res = cursor.fetchall()
                # print(res)

                if len(res) == 0:
                    evname = {'eventName': str(i), 'count': 0}
                    eventDetails.append(evname)
                    data.append(0)
                else:
                    for e in res:
                        evname = {'eventName': e[0]}
                        count = {'count': e[1]}
                        evname.update(count)
                        eventDetails.append(evname)
                        data.append(e[1])
            print("data====>", data)
            context_data = {'data': data}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
        # print("eventDetails ====>", eventDetails)
        print("data====>", data)

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time
        return render(request, 'audit_trail.html',
                      {'baseURL': baseURL, 'userlist': ulist, 'eventDetails': eventDetails, 'data': data,
                       'response': response})
    else:
        return redirect(baseURL)


def showAuditLogs(request):
    if request.session.has_key('session_key'):
        print("+++++++++++++++++++++++++++++++++++++++showAuditLogs+++++++++++++++++++++++")

        userid = request.GET.get('userid')
        ename = request.GET.get('ename')
        print("userid=====>", userid, "| ename ====>", ename)

        sdate = request.GET.get('sdate')
        edate = request.GET.get('edate')

        print("sd====>", sdate, " | ed====>", edate)

        ulist = [userid, ename, sdate, edate]
        print("userlist======>", ulist)

        cursor = connection.cursor()

        if sdate != "" and edate != "":
            query = "select Replace(EventName,'_',' ') as EventName,count(EventName) as count,Date,eventname from activity_logs_modules where userid='" + str(
                userid) + "' and cast(Date as Date) between '" + sdate + "' and '" + edate + "' group by EventName order by EventName"
            cursor.execute(query)
            print(query)
            detailsCount = cursor.fetchall()
            print(len(detailsCount))
            li = []
            for i in detailsCount:
                q = "SELECT Date FROM `activity_logs_modules` WHERE userid='" + userid + "' and eventname='" + i[
                    3] + "'  order by date desc limit 1"
                cursor.execute(q)
                # print(q)
                laston = cursor.fetchall()
                # print("#########################################################", len(laston),"\n",laston)
                li.append(laston[0])
            print("li===>", li)
            detailsCount1 = zip(detailsCount, li)

            cursor.execute(
                "select Replace(EventName, '_', ' '),deviceinfo, DATE(date) as Date, TIME(date) as Time, MONTH(date), Day(date), date from activity_logs_modules where userid = '" + userid + "' and cast(Date as Date) between '" + sdate + "' and '" + edate + "'order by Time desc ")
            detailsDates = cursor.fetchall()
            # print("detailsdate===",detailsDates)
            print("length===>", len(detailsDates))

            cursor.execute(
                "select MONTH(date), Day(date),DATE(date) as Date from activity_logs_modules where UserID = '" + userid + "' and cast(Date as Date) between '" + sdate + "' and '" + edate + "'  group by cast(date as Date), MONTH(date), Day(date) order by month(date), Day(date) desc")
            total = cursor.fetchall()
            print("length==>", len(total), "| tot ===>", total)

            # context_data = {'detailsCount1':detailsCount1,'detailsDates':detailsDates,'total':total,'lenDetailCount':len(detailsCount),'lengthTotal':len(total)}
            # return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
        else:
            query = "select Replace(EventName,'_',' ') as EventName,count(EventName) as count,Date,eventname from activity_logs_modules where userid='" + str(
                userid) + "' group by EventName order by EventName"
            cursor.execute(query)
            print(query)
            detailsCount = cursor.fetchall()
            print(len(detailsCount))
            li = []
            for i in detailsCount:
                q = "SELECT Date FROM `activity_logs_modules` WHERE userid='" + userid + "' and eventname='" + i[
                    3] + "'  order by date desc limit 1"
                cursor.execute(q)
                # print(q)
                laston = cursor.fetchall()
                # print("#########################################################", len(laston),"\n",laston)
                li.append(laston[0])
            print("li===>", li)
            detailsCount1 = zip(detailsCount, li)

            cursor.execute(
                "select Replace(EventName, '_', ' '),deviceinfo, DATE(date) as Date, TIME(date) as Time, MONTH(date), Day(date), date from activity_logs_modules where userid = '" + userid + "' order by Time desc ")
            detailsDates = cursor.fetchall()
            # print("detailsdate===",detailsDates)
            print("length===>", len(detailsDates))

            cursor.execute(
                "select MONTH(date), Day(date),DATE(date) as Date from activity_logs_modules where UserID = '" + userid + "'  group by cast(date as Date), MONTH(date), Day(date) order by month(date), Day(date) desc")
            total = cursor.fetchall()
            print("length==>", len(total), "| tot ===>", total)

        datalength = len(total)
        paginator = Paginator(total, 5)
        page = request.GET.get('page')
        print(page)
        total = paginator.get_page(page)
        print(total)
        if page:
            strt = int(page) * 5 - 5
            end = int(page) * 5
            print(strt)
            print(end)
            li = li[strt:end]
            print(li)
        print(total)

        name = "{0}".format(request.session.get('ename'))
        date_time = "{0}".format(request.session.get('date_time'))
        response = name + " " + date_time
        return render(request, 'audit_logs.html', {'baseURL': baseURL, 'userlist': ulist, 'detailsCount': detailsCount,
                                                   'detailsCount1': detailsCount1, 'detailsDates': detailsDates,
                                                   'total': total, 'lenDetailCount': len(detailsCount),
                                                   'lengthTotal': len(total), 'response': response,
                                                   'datalength': datalength})
    else:
        return redirect(baseURL)


def Encrypt_Sample(request):
    print("++++++++++++++++++++++Encrypt_Sample Called()+++++++++++++++++++++++++++++++++++++")
    if request.method == 'POST':
        t1 = request.POST.get('TextBox1')
        # type = request.POST.get('type')
        type = request.POST.get('Button1')
        b2 = request.POST.get('Button2')
        print("t1--------->", t1)
        print("type--------->", type, " |   b2------> ", b2)

        try:
            if t1 is not None:
                print("inside =======")
                if type == 'Encrypt':
                    res = object.encryptString(t1)
                else:
                    res = object.decryptString(t1)
                return render(request, 'Encryption.html', {'baseURL': baseURL, 'res': res, 't1': t1})
        except:
            return render(request, 'Encryption.html', {'baseURL': baseURL})
    else:
        return render(request, 'Encryption.html', {'baseURL': baseURL})


####################################################### IOS API's ###########################################################

#  +++++++++++++++++++++++++++++++++++++++++++++++++++IOS API Services ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# _____________________________________Pushpak____________________________

@csrf_exempt
def authenticate_june5_enc(request):
    try:
        userid = object.decryptString(request.POST.get('userid'))
        password = object.decryptString(request.POST.get('password'))
        timeStamp = object.decryptString(request.POST.get('timeStamp'))
        token = object.decryptString(request.POST.get('token'))
        res = {}

        cursor = connection.cursor()

        cursor.execute(
            "select * from `emeet_manageusers` where `userid` = '" + userid + "' and (active='true' or wipe=1) ")
        userlist = cursor.fetchall()
        userlist = list(userlist[0])
        if len(userlist) > 0:
            # plainText = "3019e42a9631c481e04db080040d5b35083cfb5f272b599f"
            # plainText = decrypt(userlist[1])
            plainText = userlist[1]
            print("plainText------------------>", plainText)
            token1 = userlist[15]
            accountstatus = userlist[25]
            print(accountstatus)
            lo = {}
            if not token1 or token1 == "":
                token2 = generate_uuid

                token1 = userid + "_" + str(token2)
                cursor.execute(
                    "update emeet_manageusers set token= '" + token1 + "' where `userid` = '" + userid + "' ")
            res["data"] = str(userid) + "|" + str(timeStamp) + "|" + str(password)
            locakedAcc = True

            # added blowfish decryption
            dec_pass = decryption(plainText)
            print('dec_pass: ', dec_pass, type(dec_pass))
            dec_passwd = dec_pass.replace('b', '').replace("'", '')

            print("dec_passwd---------->", dec_passwd)
            print("password------------>", password)
            if dec_passwd == password:
                print("inside if ======= password match ")
                lo['status'] = "true"
                if accountstatus != "" and accountstatus != None and accountstatus:
                    if accountstatus.lower() != 'true':
                        lockedAcc = UNsucess_login(userid)
                        if not locakedAcc:
                            lo['status_Message'] = "Your account is locked, Kindly contact Secretarial Team."
                        else:
                            Sucess_login(userid)
                else:
                    Sucess_login(userid)
                acc = ""
                if userlist[2] == "admin":
                    acc = getAccess(userlist[16], userlist[2])
                else:
                    acc = getAccess(userlist[17], userlist[2])

                lastlogin = userlist[24]
                wipe = userlist[28]

                dd = get_presenter(userid)
                print("dd---->", dd)
                if dd == "":
                    presentorflag = "false"
                else:
                    presentorflag = "true"
                PresenterCommittee = dd
                authcode = getauthcode(userlist[2], "true", lastlogin, wipe)
                difference = no_days_pwd(userid)
                t = 60 - difference
                print("daysssssss", t)
                if difference > 60:
                    res["expiry_flag"] = "false"
                else:
                    res["expiry_flag"] = "true"

                print("user list-->", userlist)
                res["question"] = userlist[9]
                res["answer"] = excapseStr(userlist[10])
                res["email"] = userlist[8]
                res["auth_code"] = authcode
                res["name"] = userlist[3]
                res["access"] = excapseStr(acc)
                res["company"] = company(userlist[17])
                res["token"] = token1
                res["days"] = t

                res["PresenterFlag"] = presentorflag
                res["PresenterCommittee"] = PresenterCommittee
                print(res)
                # d1={"data":"prashant|prashant_20201124191040679|Prashant@1","question":"what is your favorite color ?","answer":"prashant","email":"prashant.t@mobitrail.com","auth_code":"1","name":"Prashant Trivedi","access":"Board Committee alpha;1","company":"alpha","token":"prashant_eog2QVpv2Ej58pixvKOFQamVKiCPb81X","days":"28","expiry_flag":"true","PresenterFlag":"false","PresenterCommittee":""}

                # data = {
                #     "status": "true",
                #     "enc_data": object.encryptString(json.dumps(res, separators=(',', ':'))),
                #     "status_Message": None
                # }

                lo['enc_data'] = object.encryptString(json.dumps(res, separators=(',', ':')))
                print(object.decryptString(lo["enc_data"]))


            else:
                print("password not matched")
                lo['status'] = "false"
                lockedAcc = UNsucess_login(userid);
                print("--->", locakedAcc)
                if not locakedAcc:
                    lo['status_Message'] = "Your account is locked, Kindly contact Secretarial Team."
                else:
                    lo['status_Message'] = "Incorrect Password"

            return JsonResponse(lo)


    except:
        traceback.print_exc()
        data = {
            "status": "false",
            "enc_data": "",
            "status_Message": None
        }
        return JsonResponse(data)


@csrf_exempt
def MeetingsInfo1_enc(request):
    try:
        userid = request.POST.get('userid')
        print(userid)
        fid = ""
        token = ""
        userid1 = ""
        res = {}
        dtres = {}
        if userid == "" or not userid:
            userid1 = object.decryptString(request.form['userid'])
            fid = object.decryptString(request.form['fid'])
            token = object.decryptString(request.form['token'])
        else:
            userid1 = object.decryptString(request.POST.get('userid'))
            fid = object.decryptString(request.POST.get('fid'))
            token = object.decryptString(request.POST.get('token'))
        result = ""
        if userid != "" and userid:
            if token != "" and token:
                try:
                    userid = token.split('_')
                    cursor = connection.cursor()

                    cursor.execute(
                        "select token from emeet_manageusers where userid='" + userid1 + "' and token='" + token + "'")
                    userlist = cursor.fetchall()
                    if len(userlist) > 0:
                        strr = CurrentMeeting(fid) + PreviousMeeting(fid);
                        if strr != "" and strr:
                            result = "<info>" + strr + "</info>"
                            res['status'] = 'true'
                            dtres['token'] = userlist[0][0]
                        else:
                            result = "0"
                            res['status'] = 'true'
                            dtres['token'] = userlist[0][0]
                    else:
                        result = "Invalid token"
                        res['status'] = 'false'
                        dtres['token'] = ""
                except:
                    traceback.print_exc()
                    result = '0'
                    res['status'] = 'false'
                    dtres['token'] = ""
            else:
                result = "<error>Invalid Parameters</error>"
                res['status'] = 'false'
                dtres['token'] = ""
        else:
            result = "Invalid Parameters"
            res['status'] = 'false'
            dtres['token'] = ""
        dtres['response'] = result
        data = {
            "status": "true",
            "data": object.encryptString(json.dumps(dtres, separators=(',', ':'))),
        }
        return JsonResponse(data)

    except:
        traceback.print_exc()
        data = {
            "status": "false",
            "data": "",
        }
        return JsonResponse(data)


@csrf_exempt
def ret_dashboard(request):
    try:
        userid = request.POST.get('userid')
        print('dashbod userid--->', userid)
        fid = ""
        token = ""
        userid1 = ""
        res = {}
        dtres = {}
        if userid == "" or not userid:
            userid1 = object.decryptString(request.form['userid'])
            try:
                fid = object.decryptString(request.form['fid'])
            except:
                fid = ''
            token = object.decryptString(request.form['token'])
        else:
            userid1 = object.decryptString(request.POST.get('userid'))

            try:
                fid = object.decryptString(request.POST.get('fid'))
            except:
                fid = ''
            token = object.decryptString(request.POST.get('token'))
        res = {}
        dtres = {}
        if token != "" and token:
            cursor = connection.cursor()
            cursor.execute(
                "select * from emeet_manageusers where userid='" + userid1 + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            if len(userlist) > 0:
                dd = {}
                Forum = []
                print("dashbd userlist---> ", userlist)
                access = userlist[0][17]
                if access == "0":
                    dtres['response'] = "0"
                    res['status'] = "true"
                    dtres['token'] = token
                else:
                    if access == 'usrmanage' or access == 'admin':
                        cursor.execute(
                            "select f.fid,f.fname,f.company_id,c.abbr,c.name from emeet_forums f,emeet_company c where f.company_id=c.id and stat='true'")
                        userlist1 = cursor.fetchall()
                        for li in userlist1:
                            fr = {}
                            fr['fid'] = str(li[0])
                            fr['fname'] = li[1]
                            fr['company'] = li[3]
                            fr['companyName'] = li[4]
                            meetings = CurrentMeeting1(li[0])
                            fr['meetings'] = meetings
                            Forum.append(fr)
                    else:
                        acc = getCommittees(access)
                        print("dashboard acc---->", acc)
                        for ind, va in enumerate(acc):
                            cmny = getabr(acc[ind], 'company')
                            fr = {}
                            fr['fid'] = str(acc[ind])
                            fr['fname'] = getabr(acc[ind], 'fname') + " " + cmny
                            fr['company'] = cmny
                            fr['companyName'] = getabr(acc[ind], 'companyname')

                            meetings = CurrentMeeting1(acc[ind])
                            fr['meetings'] = meetings
                            Forum.append(fr)

                    # __________________________CALENDAR____________________________
                    Calendar = []
                    cursor.execute("select committee from emeet_manageusers where userid='" + str(userid1) + "'")
                    lis = cursor.fetchall()
                    l = ""
                    print("dashbd lis---->", lis)

                    if len(lis) > 0:
                        for ev in lis:
                            print("ev--->", ev)
                            a = ev[0].split(',')

                        l = ','.join(a)
                        print("__________________", l)
                    cursor.execute("select * from emeet_annual_meetings where fid in (" + l + ") ")
                    userlist2 = cursor.fetchall()

                    if len(userlist2) > 0:
                        for elem in userlist2:
                            cd = {}
                            cd['id'] = str(elem[0])
                            cd['fid'] = str(elem[4])
                            cd['forum'] = elem[1]
                            cd['title'] = elem[2]
                            cd['company_id'] = str(elem[6])
                            if cd['company_id'] == None or cd['company_id'] == 'None':
                                cd['company_id'] = ""
                            cd['venue'] = elem[5]
                            cd['date'] = elem[3]
                            Calendar.append(cd)
                    # ________________________________________ Shared Document ___________________________
                    Shared_doc = []
                    cursor.execute(
                        "select ms.id,ms.name,ms.link,ms.dt,ms.company,mc.name as company_name,mc.abbr from  emeet_shareddoc ms,emeet_company mc where ms.company=mc.id and ms.id in (select doc_id from emeet_document_users where userid='" + userid1 + "') order by ms.dt desc")
                    userlist3 = cursor.fetchall()
                    print("dashbd userlist3-->", userlist3)
                    if len(userlist3) > 0:
                        for elem1 in userlist3:
                            sd = {}
                            sd['id'] = str(elem1[0])
                            sd['name'] = elem1[1]
                            sd['link'] = getLink2(elem1[2], elem1[4])
                            sd['company'] = elem1[5]
                            sd['company_abbr'] = elem1[6]
                            sd['date'] = (elem1[3]).strftime("%Y/%m/%d %I:%M %p")
                            Shared_doc.append(sd)

                    print("dashboard shared doc--->", Shared_doc)
                    # ________________________________________ News ___________________________
                    news = []
                    cursor.execute(
                        "select mn.id,mn.title,mn.description,mn.publishdate,mn.company,mn.insertdate,mc.name,mc.abbr from emeet_news mn,emeet_company mc where mn.company=mc.id order by mn.insertDate desc")
                    userlist4 = cursor.fetchall()
                    if len(userlist4) > 0:
                        for elem2 in userlist4:
                            nw = {}
                            nw['id'] = str(elem2[0])
                            nw['title'] = elem2[1]
                            nw['description'] = elem2[3]
                            nw['publish_Date'] = elem2[4]
                            nw['company'] = elem2[6]
                            nw['company_abbr'] = elem2[7]
                            nw['date'] = elem2[5]

                            news.append(nw)
                    # ________________________________________ MOM ___________________________
                    Mom = []
                    cursor.execute("select * from emeet_mom where fid='" + str(fid) + "'")
                    userlist5 = cursor.fetchall()
                    if len(userlist5) > 0:
                        for elem3 in userlist5:
                            mo = {}
                            mo['id'] = str(elem3[0])
                            mo['mid'] = str(elem3[1])
                            mo['pdf'] = elem3[2]
                            mo['fid'] = str(elem3[3])
                            mo['ver'] = elem3[4]
                            mo['approved'] = elem3[5]
                            Mom.append(mo)
                    # ________________________________________ MOM Draft ___________________________
                    Mom_draft = []
                    cursor.execute(
                        "select * from emeet_mom1 where id=(select mom_id from emeet_mapping_agenda where userid='" + userid1 + "' order by id desc limit 1) and fid='" + str(
                            fid) + "' and expirydate>now()")
                    userlist6 = cursor.fetchall()
                    if len(userlist6) > 0:
                        for elem4 in userlist6:
                            mod = {}
                            mod['mid'] = str(elem4[1])
                            mod['title'] = elem4[8]
                            mod['pdf'] = elem4[2]
                            mod['status'] = elem4[11]
                            mod['ver'] = elem4[4]
                            mod['expiry_Date'] = elem4[7]

                            Mom_draft.append(mod)
                    # ________________________________________ Notification ___________________________
                    notification = []

                    dd['Committee'] = Forum
                    dd['Calendar'] = Calendar
                    dd['Shared_Document'] = Shared_doc
                    dd['News'] = news
                    dd['Notification'] = notification
                    dd['Mom_draft'] = Mom_draft
                    dd['mom'] = Mom
                    dtres['response'] = dd
                    res['status'] = 'true'
                    dtres['token'] = token

            else:
                dtres['response'] = "Invalid Token"
                res['status'] = 'false'
                dtres['token'] = ''
        # res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # print("dtres---->",dtres)
        res['data'] = object.encryptString(str(dtres))
        return JsonResponse(res)
    except:
        return HttpResponse(traceback.format_exc())


#
# @csrf_exempt
# def add_user_ver_enc(request):
#     try:
#         js = request.POST.get('json')
#
#         print("add_user_ver_enc js----->",js)
#         if js == "" or not js:
#             js = object.decryptString(request.form['json'])
#         else:
#             js = object.decryptString(request.POST.get('json'))
#         name = ""
#         udid = ""
#         ver = ""
#         token = ""
#         usrtoken = ""
#         js.strip('||')
#         print("j type---->",js,type(js))
#         j = json.loads(js)
#         name = j['name']
#         udid = j['udid']
#         ver = j['ver']
#         usrtoken = j['usrtoken']
#         token = j['token']    # requires for notification
#         res = {}
#         dtres = {}
#         if usrtoken and usrtoken != "":
#             userid = usrtoken.split('_')
#             cursor = connection.cursor()
#             cursor.execute(
#                 "select token from emeet_manageusers where userid='" + userid[0] + "' and token='" + usrtoken + "'")
#             userlist = cursor.fetchall()
#             print("1")
#             if len(userlist) > 0:
#                 cursor.execute("Select * from emeet_usr_ver where name='" + name + "'")
#                 userlist1 = cursor.fetchall()
#                 print("2")
#                 if len(userlist1) > 0:
#                     print("3")
#                     a = cursor.execute(
#                         "Update emeet_usr_ver set udid='" + udid + "',ver='" + ver + "',token='" + token + "' where name='" + name + "'")
#                     if a == 1:
#                         dtres['response'] = 'true'
#                         dtres['token'] = userlist[0][0]
#                         res['status'] = 'true'
#                     else:
#                         dtres['response'] = 'false'
#                         res['status'] = 'false'
#                 else:
#                     print("4")
#                     a = cursor.execute(
#                         "Insert into emeet_usr_ver(name,udid,ver,token) values('" + name + "','" + udid + "','" + ver + "','" + token + "')")
#                     if a == 1:
#                         print("5")
#                         dtres['response'] = 'true'
#                         dtres['token'] = userlist[0][0]
#                         res['status'] = 'true'
#                     else:
#                         print("6")
#                         dtres['response'] = 'false'
#                         res['status'] = 'false'
#             else:
#                 print("7")
#                 dtres['response'] = 'false'
#                 res['status'] = 'false'
#         else:
#             print("8")
#             dtres['response'] = '<error>Invalid Parameters</error>'
#             res['status'] = 'false'
#         res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
#         return JsonResponse(res)
#     except:
#         traceback.print_exc()

@csrf_exempt
def add_user_ver_enc(request):
    try:
        j = request.POST.get('json')
        if j == "" or not j:
            j = object.decryptString(request.form['json'])
        else:
            j = object.decryptString(request.POST.get('json'))
        name = ""
        udid = ""
        ver = ""
        token = ""
        usrtoken = ""
        platform = ""

        j = json.loads(j)
        name = j['name']
        udid = j['udid']
        ver = j['ver']
        usrtoken = j['usrtoken']
        token = j['token']
        platform = j['platform']

        res = {}
        dtres = {}
        if usrtoken and usrtoken != "":
            userid = usrtoken.split('_')
            cursor = connection.cursor()
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid[0] + "' and token='" + usrtoken + "'")
            userlist = cursor.fetchall()
            print("1")
            if len(userlist) > 0:
                cursor.execute("Select * from emeet_usr_ver where name='" + name + "'")
                userlist1 = cursor.fetchall()
                print("2")
                if len(userlist1) > 0:
                    print("3")
                    a = cursor.execute(
                        "Update emeet_usr_ver set udid='" + udid + "',ver='" + ver + "',token='" + token + "',platform='" + platform + "' where name='" + name + "'")
                    if a == 1:
                        dtres['response'] = 'true'
                        dtres['token'] = userlist[0][0]
                        res['status'] = 'true'
                        multipleNotification(getAndroidTokens(name), "emeeting", "test messge from python")
                    else:
                        dtres['response'] = 'false'
                        res['status'] = 'false'
                else:
                    print("4")
                    a = cursor.execute(
                        "Insert into emeet_usr_ver(name,udid,ver,token,platform) values('" + name + "','" + udid + "','" + ver + "','" + token + "','" + platform + "')")
                    if a == 1:
                        print("5")
                        dtres['response'] = 'true'
                        dtres['token'] = userlist[0][0]
                        res['status'] = 'true'
                        multipleNotification(getAndroidTokens(name), "emeeting", "test messge from python")
                    else:
                        print("6")
                        dtres['response'] = 'false'
                        res['status'] = 'false'
            else:
                print("7")
                dtres['response'] = 'false'
                res['status'] = 'false'
        else:
            print("8")
            dtres['response'] = '<error>Invalid Parameters</error>'
            res['status'] = 'false'
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)
    except:
        traceback.print_exc()


def getAndroidTokens(user):
    token = ""
    qu = "select distinct (token) from emeet_usr_ver where  name in ('" + user + "') and token!='' and lower(platform) = 'android'";
    cursor = connection.cursor()
    cursor.execute(qu)
    userlist = cursor.fetchall()

    for u in userlist:
        token = u[0] + ","

    if token != "" and not token:
        token = token[0, len(token) - 1]
    tokenlist = token.rstrip(",").split(",")
    print("tokenlist---------->", tokenlist)
    return tokenlist


@csrf_exempt
def ret_UserAccess(request):
    j = request.POST.get('json')
    print("user access j--->", j)
    if j == "" or not j:
        j = object.decryptString(request.form['json'])
    else:
        j = object.decryptString(request.POST.get('json'))
    j = json.loads(j)
    res = {}
    dtres = {}
    try:
        cursor = connection.cursor()
        cursor.execute("select Print from emeet_manageusers where  token='" + j['usrtoken'] + "'")
        userlist = cursor.fetchall()

        if len(userlist) > 0:
            a = userlist[0][0]
            if a == 0:
                a = 'false'
            if a == 1:
                a = 'true'
            res['status'] = 'true'
            dtres['token'] = j['usrtoken']
            dtres['response'] = a
        else:
            res['status'] = 'false'
            dtres['token'] = j['usrtoken']
            dtres['response'] = "false"

    except:
        traceback.print_exc()
        dtres['token'] = ""
        dtres['response'] = "Invalid parameters"
        res['status'] = 'false'

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    return JsonResponse(res)


@csrf_exempt
def mpdf_enc(request):
    res = {}
    dtres = {}
    try:
        mid = request.POST.get('mid')
        token = ""

        if mid == "" or not mid:
            mid = object.decryptString(request.form['mid'])
            token = object.decryptString(request.form['token'])
        else:
            mid = object.decryptString(request.POST.get('mid'))
            token = object.decryptString(request.POST.get('token'))
        fid = getFID(mid)
        if token and token != "":
            userid = token.split('_')
            cursor = connection.cursor()
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            if len(userlist) > 0:
                cursor.execute("select * from emeet_Level0 where mid='" + mid + "'  order by ag_id")
                userlist1 = cursor.fetchall()

                xmlstr = ""
                if len(userlist1) > 0:
                    for a in userlist1:
                        strr = isExist(a[4], mid)
                        if strr != "" or strr:
                            xmlstr += strr + ","
                        if hasChild(a[0], "1"):
                            xmlstr += xmlstrLevel1(a[0], fid, mid)
                    cursor.execute("Select * from emeet_mom where mid='" + mid + "'")
                    userlist2 = cursor.fetchall()
                    if len(userlist2) > 0:
                        xmlstr += isExist(userlist2[0][2], mid) + ","
                if xmlstr and xmlstr != "":
                    xmlstr = xmlstr[:-1]
                xmlstr = Escapestring(xmlstr)
                dtres['response'] = xmlstr.replace('/', '\\')
                dtres['token'] = userlist[0][0]
                res['status'] = 'true'
            else:
                dtres['response'] = "false"
                res['status'] = 'false'

        else:

            dtres['response'] = '<error>Invalid Parameters</error>'
            res['status'] = 'false'


    except:
        traceback.print_exc()
        dtres['response'] = traceback.format_exc()
        res['status'] = 'false'
    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))

    return JsonResponse(res)


def connectServer():
    print("server connect")
    import asyncio
    import websockets
    connected = set()

    async def server(websocket, path):
        # Register.
        connected.add(websocket)
        try:
            async for message in websocket:
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f'Got a new MSG FOR YOU: {message}')
        finally:
            # Unregister.
            connected.remove(websocket)

    start_server = websockets.serve(server, base11, 8002)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


@csrf_exempt
def agenda_enc(request):
    res = {}
    dtres = {}
    try:
        mid = request.POST.get('mid')
        token = ""

        if mid == "" or not mid:
            mid = object.decryptString(request.form['mid'])
            token = object.decryptString(request.form['token'])
        else:
            mid = object.decryptString(request.POST.get('mid'))
            token = object.decryptString(request.POST.get('token'))

        # base12 = "/d6f183914969.ngrok.io"
        """ for websocket connection """

        #res['connectionURL'] = "wss://393dfbcfa94d.ngrok.io/ws/chat/" + mid + "/"
        res['connectionURL'] = "http://125.99.153.203:80/ws/chat/" + mid + "/"

        if token and token != "":
            userid = token.split('_')
            cursor = connection.cursor()
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            if len(userlist) > 0:

                query = "select l.ag_id,l.title,l.doc,l.fid,l.mid,l.descr,l.version,l.aid,(select userid from  emeet_mapping_agendaaccess ag where l.ag_id = ag.ag_id and ag.userid = '" + \
                        userid[
                            0] + "') as userid ,(case when code.name = '0' or code.name is null then '' else code.name end) as cname,(case when code.colorcode = '0' or code.colorcode is null then '' else code.colorcode end) as colorcode from emeet_level0 l left join emeet_agcolorcodes code on l.ColorId = code.id where l.mid = '" + str(
                    mid) + "' and ag_id not in ( select ag_id from  emeet_mapping_agendaaccess ag where l.ag_id = ag.ag_id and ag.userid = '" + \
                        userid[0] + "') order by l.aid"
                print("sql query------>", query)
                cursor.execute(query)

                userlist1 = cursor.fetchall()
                print("userlist1---> ", userlist1)
                rowcount = len(userlist1)
                startxml = "<info>"
                endxml = "</info>"
                xmlstr = ""
                if rowcount > 0:
                    for a in userlist1:
                        print("_+_+_+_+_+_++++++++++++++++++", a[8])
                        if not a[8] or a[8] == "":
                            condition = True
                        else:
                            condition = False
                        print(condition)
                        if condition:
                            print("agid--->", a[0])
                            xmlstr += "<agenda name=\"" + excapseStr(a[7]) + "." + excapseStr(str(a[1])) + "\" pdf=\"" + \
                                      a[
                                          2] + "\" url=\"" + getURL(a[3], a[4],
                                                                    a[2]) + "\" level=\"0\" desc=\"" + excapseStr(
                                a[5]) + "\" id=\"" + excapseStr(a[0]) + "\" v=\"" + excapseStr(
                                a[6]) + "\" srno=\"" + excapseStr(a[7]) + "\" colorname=\"" + excapseStr(
                                a[9]) + "\" colorcode=\"" + excapseStr(a[10]) + "\">"
                        else:
                            xmlstr += "<agenda name=\"" + excapseStr(a[7]) + "." + excapseStr(
                                a[1]) + "\" pdf=\"\" url=\"\" level=\"0\" desc=\"" + excapseStr(
                                a[5]) + "\" id=\"" + excapseStr(a[0]) + "\" v=\"" + excapseStr(
                                a[6]) + "\" srno=\"" + excapseStr(a[7]) + "\">"

                        if hasChild(a[0], '1'):
                            xmlstr += BxmlstrLevel1(a[0], a[3], a[4], excapseStr(a[7]), condition)

                        xmlstr += "</agenda>"
                    cursor.execute("Select * from emeet_mom where mid='" + mid + "' and approved='approved'")
                    userlist1 = cursor.fetchall()
                    if len(userlist1) > 0:
                        xmlstr += "<agenda name=\"" + "MOM" + "\" pdf=\"" + userlist1[0][2] + "\" url=\"" + getURL(
                            userlist1[0][3], userlist1[0][1], userlist1[0][
                                2]) + "\" level=\"0\" desc=\"" + "" + "\" id=\"" + "-1" + "\" dt1=\"" + "1900-04-10 10:23:00" + "\" dt2=\"" + "1900-05-10 10:23:00" + "\" v=\"" + excapseStr(
                            userlist1[0][4]) + "\">"
                        xmlstr += "</agenda>"
                else:
                    xmlstr += "<agenda>No Agendas Found</agenda>"
                xmlstr = Escapestring(xmlstr)
                dtres['response'] = startxml + xmlstr + endxml

                res['status'] = 'true'
                dtres['token'] = userlist[0][0]
            else:
                dtres['response'] = 'false'
                res['status'] = 'false'
        else:
            dtres['response'] = "<error>Invalid Parameters</error>"
            res['status'] = 'false'

        # print("dtres-->",json.dumps(dtres))
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # print(object.decryptString(res['data']))
        print("agenda res---------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()
        dtres['response'] = "<error>Invalid Parameters</error>"
        res['status'] = 'false'
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)


@csrf_exempt
def ret_notes2_new_enc(request):
    res = {}
    dtres = {}
    N = {}
    try:
        userid = request.POST.get('userid')
        fid = ""
        mid = ""
        flag = ""
        token = ""

        if userid == "" or not userid:
            userid = object.decryptString(request.form['userid'])
            fid = object.decryptString(request.form['fid'])
            mid = object.decryptString(request.form['mid'])
            # flag = object.decryptString(request.form['flag'])
            token = object.decryptString(request.form['token'])
        else:
            userid = object.decryptString(request.POST.get('userid'))
            fid = object.decryptString(request.POST.get('fid'))
            mid = object.decryptString(request.POST.get('mid'))
            # flag = object.decryptString(request.POST.get('flag'))
            token = object.decryptString(request.POST.get('token'))
        q = ""
        if token and token != "":
            userid1 = token.split('_')
            cursor = connection.cursor()
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            notes = []
            dt = {}
            dt['uniqId'] = ""
            dt['refId'] = ""
            dt['DeviceId'] = ""
            dt['text'] = ""
            dt['point1'] = ""
            dt['point2'] = ""
            dt['modDate'] = ""
            dt['updateFlag'] = ""
            dt['page'] = ""
            dt['agenda_title'] = ""
            dt['ag_id'] = ""
            dt['level'] = ""
            dt['docVersion'] = ""

            dt['filePath'] = ""
            dt['userid'] = ""
            dt['username'] = ""
            dt['publicflag'] = ""
            if len(userlist) > 0:
                if True:
                    if not flag or flag == "":
                        print("11")
                        query = "select en.*,(select ename from emeet_manageusers where userid=en.userid) as ename  from emeet_noting en where en.userid='" + userid + "' and en.mid = '" + str(
                            mid) + "' and en.flag in('0','i') and en.publicflag=1 order by en.level, en.ag_id"

                        print("query-->", query)
                        cursor.execute(query)
                        # cursor.execute(
                        #     "select en.*,(select ename from emeet_manageusers where userid=en.userid) as ename  from emeet_noting en where en.userid='" + userid + "' and en.mid = '" + str(
                        #         mid) + "' and en.flag in('0','i') or (userid!='" + userid + "' and en.publicflag=1) order by en.level, en.ag_id")
                        userlist1 = cursor.fetchall()
                        title = ""
                        print("userlist1---->", userlist1)
                        for a in userlist1:
                            level = a[2]
                            ag_id = a[1]

                            print("a---->", a)
                            if str(level) == "0":
                                print("level 0 a")
                                cursor.execute("select * from emeet_level0 where ag_id='" + str(ag_id) + "'")
                                userlist2 = cursor.fetchall()
                                print("l0 userlist2------>", userlist2)
                                if len(userlist2) > 0:
                                    title = str(userlist2[0][7]) + "." + str(userlist2[0][1])
                            elif level == "1":
                                print("level 1 b")
                                cursor.execute("select * from emeet_level1 where ag_id='" + str(ag_id) + "'")
                                userlist2 = cursor.fetchall()
                                print("l1 userlist2------>", userlist2)
                                if len(userlist2) > 0:
                                    cursor.execute(
                                        "select * from emeet_level0 where ag_id='" + str(userlist2[0][3]) + "'")
                                    userlist3 = cursor.fetchall()
                                    if len(userlist3) > 0:
                                        title = str(userlist3[0][7]) + ".(" + getalphaID(userlist2[0][6]) + ") " + str(
                                            userlist2[0][1])
                            else:
                                print("level 2 c")
                                cursor.execute("select * from emeet_level2 where ag_id='" + str(ag_id) + "'")
                                userlist2 = cursor.fetchall()
                                print("l2 userlist2------>", userlist2)
                                if len(userlist2) > 0:
                                    cursor.execute(
                                        "select * from emeet_level1 where ag_id='" + str(userlist2[0][3]) + "'")
                                    userlist3 = cursor.fetchall()
                                    if len(userlist3) > 0:
                                        cursor.execute(
                                            "select * from emeet_level0 where ag_id='" + str(userlist3[0][3]) + "'")
                                        userlist4 = cursor.fetchall()
                                        if len(userlist4) > 0:
                                            title = str(userlist4[0][7]) + ".(" + getalphaID(
                                                userlist3[0][6]) + ")(" + intToRoman(userlist2[0][6]) + ") " + str(
                                                userlist2[0][1])
                            print("userlist2------>", userlist2)
                            deviceid = a[11]
                            if not deviceid:
                                deviceid = ""

                            publicflag = a[13]
                            if publicflag == "0":
                                publicflag = "False"
                            else:
                                publicflag = "True"
                            if len(userlist2) > 0:
                                print("for loop notes-->", notes)
                                print("1====", a)
                                dt = {}
                                dt['uniqId'] = a[4]
                                dt['refId'] = a[4]
                                dt['DeviceId'] = deviceid
                                dt['text'] = a[5]
                                dt['point1'] = a[6]
                                dt['point2'] = a[7]
                                dt['modDate'] = a[8].strftime("%d/%m/%Y %I:%m:%S %p")
                                dt['updateFlag'] = a[9]
                                dt['page'] = a[10]
                                dt['agenda_title'] = title
                                dt['filePath'] = ""
                                dt['docVersion'] = ""

                                dt['ag_id'] = a[1]
                                dt['level'] = a[2]
                                dt['userid'] = a[3]
                                dt['username'] = a[14]
                                dt['publicflag'] = publicflag
                                notes.append(dt)
                                print("in notes--->", notes)
                    else:
                        print("12")
                        cursor.execute("select * from emeet_noting where userid='" + userid + "' and mid = '" + str(
                            mid) + "'   and flag in('0','i') order by level, ag_id ")
                        userlist1 = cursor.fetchall()
                        for a in userlist1:
                            level = a[2]
                            ag_id = a[1]

                            if level == "0":
                                q2 = "select title from emeet_level0 whre ad_id='" + str(ag_id) + "'"

                            elif level == "1":
                                q2 = "select title from emeet_level1 whre ad_id='" + str(ag_id) + "'"

                            else:
                                q2 = "select title from emeet_level2 whre ad_id='" + str(ag_id) + "'"

                            cursor.execute(q2)
                            userlist2 = cursor.fetchall()
                            print("notes userlist2-->", userlist2)
                            title = userlist2[0][0]
                            deviceid = a[11]
                            if not deviceid:
                                deviceid = ""

                            dt['uniqId'] = a[4]
                            dt['refId'] = a[4]
                            dt['DeviceId'] = deviceid
                            dt['text'] = a[5]
                            dt['point1'] = a[6]
                            dt['point2'] = a[7]
                            dt['modDate'] = a[8].strftime("%d/%m/%Y %I:%m:%S %p")
                            dt['updateFlag'] = a[9]
                            dt['page'] = a[10]
                            dt['filePath'] = ""
                            dt['docVersion'] = ""
                            dt['agenda_title'] = title
                            dt['ag_id'] = a[1]
                            dt['level'] = a[2]
                            notes.append(dt)
                print("notes--->", notes)
                N['notings'] = notes
                res['status'] = 'true'
                dtres['token'] = userlist[0][0]
                dtres['response'] = N
            else:
                dtres['response'] = 'false'
                res['status'] = 'false'
        else:
            dtres['response'] = '<error>Invalid parameters</error>'
            res['status'] = 'false'

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)


    except:
        traceback.print_exc()
        dtres['response'] = "<error>Invalid Parameters</error>"
        res['status'] = 'false'
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)


def Escapestring(xmlstr):
    xmlstr = xmlstr.replace("''", "'");
    return xmlstr.replace('&', '&amp;')


def BxmlstrLevel1(id, fid, mainid, srno, condition):
    cursor = connection.cursor()
    cursor.execute(
        "select main.*,(case when code.name = '0' or code.name is null then '' else code.name end) as cname,(case when code.colorcode = '0' or code.colorcode is null then '' else code.colorcode end) as colorcode from emeet_level1 main left join emeet_agcolorcodes code on main.ColorId = code.id where parent = '" + str(
            id) + "' order by aid")
    userlist = cursor.fetchall()
    xmlstr1 = ""
    for a in userlist:
        parent_srno = srno + "." + excapseStr(getalphaID(a[6]))
        if condition:
            print("level1 agid--->", a[0])
            xmlstr1 += "<sagenda name=\"" + excapseStr(getalphaID(a[6])) + ") " + excapseStr(a[1]) + "\" pdf=\"" + a[
                4] + "\" url=\"" + getURL(fid, mainid, a[4]) + "\" level=\"1\" desc=\"" + excapseStr(
                a[2]) + "\" id=\"" + excapseStr(a[0]) + "\" v=\"" + excapseStr(
                a[5]) + "\" srno=\"" + srno + "\" colorname=\"" + excapseStr(a[8]) + "\" colorcode=\"" + excapseStr(
                a[9]) + "\">"
        else:
            xmlstr1 += "<sagenda name=\"" + excapseStr(getalphaID(a[6])) + ") " + excapseStr(
                a[1]) + "\" pdf=\"\" url=\"\" level=\"1\" desc=\"" + excapseStr(a[2]) + "\" id=\"" + excapseStr(
                a[0]) + "\" v=\"" + excapseStr(a[5]) + "\" srno=\"" + srno + "\" colorname=\"" + excapseStr(
                a[8]) + "\" colorcode=\"" + excapseStr(a[9]) + "\">"
        if hasChild(a[0], "2"):
            xmlstr1 += BxmlstrLevel2(a[0], id, fid, mainid, parent_srno, condition)
        xmlstr1 += "</sagenda>"
    return xmlstr1


def BxmlstrLevel2(id, ids, fid, mainid, parent_srno, condition):
    cursor = connection.cursor()
    cursor.execute(
        "select main.*,(case when code.name = '0' or code.name is null then '' else code.name end) as cname,(case when code.colorcode = '0' or code.colorcode is null then '' else code.colorcode end) as colorcode from emeet_level2 main left join emeet_agcolorcodes code on main.ColorId = code.id where parent = '" + str(
            id) + "' order by aid")
    userlist = cursor.fetchall()
    xmlstr1 = ""
    for a in userlist:
        val = a[6]
        rom = intToRoman(int(val))

        xmlstr1 += "<ssagenda name=\"(" + rom.lower() + ") " + a[1] + "\" "
        if condition:
            print("level2 agid-->", a[0])
            xmlstr1 += "pdf=\"" + a[4] + "\" "
            xmlstr1 += "url=\"" + getURL(fid, mainid, a[4]) + "\" level=\"2\" "
        else:
            xmlstr1 += "pdf=\"\" "
            xmlstr1 += "url=\"\" level=\"2\" "
        xmlstr1 += "colorname=\"" + a[8] + "\" "
        xmlstr1 += "colorcode=\"" + a[9] + "\" "
        xmlstr1 += "desc=\"" + str(a[2]) + "\" id=\"" + str(a[0]) + "\" v=\"" + str(a[5]) + "\" srno=\"" + str(
            parent_srno) + "\">"
        xmlstr1 += "</ssagenda>"
    return xmlstr1


def xmlstrLevel1(id, fid, mid):
    cursor = connection.cursor()
    cursor.execute("select * from emeet_level1 where parent='" + str(id) + "' order by ag_id")
    userlist = cursor.fetchall()
    xmlstr1 = ""
    if len(userlist) > 0:
        for a in userlist:
            strr = isExist(a[4], mid)
            if strr != "" or strr:
                xmlstr1 += strr + ","
            if hasChild(a[0], "2"):
                xmlstr1 += xmlstrLevel2(a[0], fid, mid)
    return xmlstr1


def xmlstrLevel2(id, fid, mid):
    cursor = connection.cursor()
    cursor.execute("select * from emeet_level2 where parent='" + str(id) + "' order by ag_id")
    userlist = cursor.fetchall()
    xmlstr2 = ""
    if len(userlist) > 0:
        for a in userlist:
            strr = isExist(a[4], mid)
            if strr != "" or strr:
                xmlstr2 += strr + ","

    return xmlstr2


def hasChild(a, level):
    print("has child--->", a, level)
    cursor = connection.cursor()
    cursor.execute("select * from emeet_level" + str(level) + " where parent='" + str(a) + "'")
    userlist = cursor.fetchall()
    print("list--->", userlist)
    if len(userlist) > 0:
        return True
    else:
        return False


def isExist(doc, mid):
    fid = getFID(mid)
    path = basepath + "static/resources/" + getFname(str(fid)) + "/" + str(mid) + "/" + str(doc)
    if doc == "" or not doc:
        return ""
    else:
        return path


def getFID(mid):
    cursor = connection.cursor()
    cursor.execute("select fid from emeet_meeting where id='" + str(mid) + "'")
    userlist = cursor.fetchall()
    return userlist[0][0]


def getLink2(t1, t2):
    print("shre doc--->", t1, '--->', t2)
    return base11 + baseURL + "static/SharedDocs/" + str(t2) + "/" + str(t1)


def getabr(fid, flag):
    if fid != "" and fid:
        cursor = connection.cursor()
        commi = []
        cursor.execute(
            "select f.fname,c.abbr,c.name from emeet_forums f,emeet_company c where f.company_id=c.id and fid='" + str(
                fid) + "'")
        userlist = cursor.fetchall()
        if len(userlist) > 0:
            if flag == 'fname':
                return userlist[0][0]
            elif flag == 'companyname':
                return userlist[0][2]
            else:
                return userlist[0][1]
        else:
            return ""

    else:
        return ""


def getCommittees(access):
    cursor = connection.cursor()
    commi = []
    cursor.execute("select fid from emeet_forums where fid in (" + access + ") and stat='true' order by fid")
    userlist = cursor.fetchall()
    for a in userlist:
        commi.append(a[0])
    return commi


def no_days_pwd(userid):
    cursor = connection.cursor()

    cursor.execute("select pwd_dt from emeet_manageusers where `userid`='" + userid + "'")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        try:
            dt_Set = userlist[0][0]
            difference = (datetime.datetime.now() - dt_Set)
            print("))))))))))))))))))))))))))", difference.days)
            return difference.days
        except:
            return 0
    else:
        return 0


def CurrentMeeting1(fid):
    m1 = []
    cursor = connection.cursor()
    print("curr meet fid--->", fid)

    cursor.execute(
        "select dt,id,title from emeet_meeting where DATEDIFF(now(),dt)<=days and DATEDIFF(now(),dt)>=0 and `fid`='" + str(
            fid) + "' and status='true' order by dt")
    userlist = cursor.fetchall()
    for a in userlist:
        m = {}
        dt123 = a[0]
        m['title'] = a[2]
        m['mid'] = str(a[1])
        cursor.execute("Select * from emeet_mom where mid='" + str(a[1]) + "'")
        userlist1 = cursor.fetchall()
        if len(userlist1) > 0:
            m['url'] = getURL(fid, a[1], userlist1[0][2])
            m['ver'] = excapseStr(userlist1[0][4])
        else:
            m['url'] = ""
            m['ver'] = ""
        m['date'] = dt123.strftime("%m/%d/%Y %I:%M:%S %p")
        m['status'] = "0"
        m1.append(m)
    cursor.execute(
        "select dt,id,title from emeet_meeting where date(DATE_ADD(dt, INTERVAL days DAY))<CURDATE() and `fid`='" + str(
            fid) + "' and status='true' order by dt desc limit 1")
    userlist2 = cursor.fetchall()
    for a in userlist2:
        m = {}
        dt123 = a[0]
        m['title'] = a[2]
        m['mid'] = str(a[1])
        cursor.execute("Select * from emeet_mom where mid='" + str(a[1]) + "'")
        userlist1 = cursor.fetchall()
        if len(userlist1) > 0:
            m['url'] = getURL(fid, a[1], userlist1[0][2])
            m['ver'] = excapseStr(userlist1[0][4])
        else:
            m['url'] = ""
            m['ver'] = ""
        m['date'] = dt123.strftime("%m/%d/%Y %I:%M:%S %p")
        m['status'] = "0"
        m1.append(m)
    return m1


def getURL(fid, mid, filename):
    if filename and filename != "":
        # url = "http://127.0.0.1:8000/static/resources/" + getFname(str(fid)) + "/" + str(mid) + "/" + filename
        url = base11 + "/static/resources/" + getFname(str(fid)) + "/" + str(mid) + "/" + filename
        return url
    else:
        return ""


def getFname(fid):
    cursor = connection.cursor()
    cursor.execute("select fname from emeet_Forums where fid = '" + fid + "'")
    userlist = cursor.fetchall()
    return userlist[0][0]


def CurrentMeeting(fid):
    xml = ""

    cursor = connection.cursor()

    cursor.execute(
        "select dt,id,title from emeet_meeting where DATEDIFF(now(),dt)<=days and DATEDIFF(now(),dt)>=0 and `fid`='" + str(
            fid) + "' and status='true' order by dt")
    userlist = cursor.fetchall()

    if len(userlist) > 0:
        for a in userlist:
            xml += "<id title=\"" + str(a[2]) + "\" mid=\"" + str(a[1]) + "\" date=\"" + str(
                a[0].strftime("%m/%d/%Y %I:%M:%S %p")) + "\" status=\"0\" />"
    return xml


def PreviousMeeting(fid):
    xml = ""
    cursor = connection.cursor()

    cursor.execute(
        "select dt,id,title from emeet_meeting where date(DATE_ADD(dt, INTERVAL days DAY))<CURDATE() and `fid`='" + str(
            fid) + "' and status='true' order by dt desc limit 1")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        for a in userlist:
            xml += "<id title=\"" + str(a[2]) + "\" mid=\"" + str(a[1]) + "\" date=\"" + str(
                a[0].strftime("%m/%d/%Y %I:%M:%S %p")) + "\" status=\"1\" />"
    return xml


def generate_uuid():
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [8, 4, 4, 4, 12]
    for n in uuid_format:
        for i in range(0, n):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])

    return random_string


def getauthcode(access, status, lastlogin, wipe):
    if lastlogin and wipe == 0:
        print(lastlogin)
        if "." in str(lastlogin):
            lldate = datetime.datetime.strptime(str(lastlogin), "%Y-%m-%d  %H:%M:%S.%f")
        else:
            lldate = datetime.datetime.strptime(str(lastlogin), "%Y-%m-%d  %H:%M:%S")

        print(lldate)
        difference = datetime.datetime.now() - lldate
        print(difference.days)
        if difference.days > 30:
            return "7"
        else:
            if access == "0" or access == "" or not access:
                return "3"
            else:
                if status.lower() == "true":
                    return "1"
                else:
                    return "3"

    else:
        if not wipe:
            if access == "0" or access == "" or not access:
                return "3"
            else:
                if status == "true":
                    return "1"
                else:
                    return "3"
        else:
            return "8"


def excapseStr(xml):
    xml = str(xml)
    xml = xml.replace("''", "'");
    xml = xml.replace("\"", "&quot;");
    xml = xml.replace("<", "&lt;");
    xml = xml.replace(">", "&gt;");
    return xml.replace("&", "&amp;");


def UNsucess_login(userid):
    try:
        counter = 0
        cursor = connection.cursor()
        cursor.execute(
            "select *,TIMESTAMPDIFF(MINUTE,LUA,now()) as diff from emeet_manageusers where userid='" + userid + "' and active='True'")
        userlist = cursor.fetchall()
        userlist = list(userlist[0])
        if len(userlist) > 0:
            diff_count = userlist[30]
            if userlist[23]:
                dd = userlist[23]
            else:
                dd = "0"
            if int(dd) < 5:
                counter = int(dd) + 1
                a = cursor.execute("update emeet_manageusers set `attemptcount`=" + str(
                    counter) + " , `LUA`=now() where `userid`='" + str(userid) + "'")
                return True
            else:
                if diff_count >= 5:
                    a = cursor.execute(
                        "update emeet_manageusers set `accountStatus`='True' where `userid`='" + userid + "'")
                    return True
                else:
                    a = cursor.execute(
                        "update emeet_manageusers set `accountStatus`='False' where `userid`='" + userid + "'")
                    return False
        else:
            return False
    except:

        traceback.print_exc()
        return False


def Sucess_login(userid):
    try:
        cursor = connection.cursor()
        a = cursor.execute(
            "update emeet_manageusers set `attemptcount`=0 , `LUA`=now() where `userid`='" + userid + "'")
        return True
    except:
        traceback.print_exc()
        return False


def getAccess(commitee, access):
    print("in getAccess")
    print(commitee)
    xml = ""
    cursor = connection.cursor()
    if access == "0":
        xml += "0"
    else:
        if access == "usrmanage" or access == "admin":
            cursor.execute(
                "select f.fid,Replace(f.fname,'emeet_',''),c.abbr from emeet_forums f,emeet_company c where f.company_id=c.id and f.stat='true' and f.approved='approved' order by f.fid")
            userlist = cursor.fetchall()
            userlist = list(userlist)
            for ele in userlist:
                xml += str(ele[1]) + ";" + str(ele[2]) + ";"
            xml = xml[:-1]
        else:
            cursor.execute(
                "select f.fid,Replace(f.fname,'emeet_','') as fname,c.abbr from emeet_forums f,emeet_company c where f.company_id=c.id and f.stat='true' and f.approved='approved' and fid in (" + commitee + ") order by f.fid")
            userlist = cursor.fetchall()
            userlist = list(userlist)
            if len(userlist) > 0:
                for ele in userlist:
                    xml += str(ele[1]) + " " + str(ele[2]) + ";" + str(ele[0]) + ";"
                xml = xml[:-1]
    xml += ""
    return xml


def get_presenter(userid):
    cursor = connection.cursor()
    cursor.execute("select * from emeet_forums where presentor = '" + userid + "'")
    userlist = cursor.fetchall()
    presentor = ""
    if len(userlist) > 0:
        print("userlist-- ", userlist)
        for a in userlist:
            presentor += str(a[0]) + ","
        presentor = presentor[:-1]
    return presentor


def company(access):
    str1 = ""
    cursor = connection.cursor()
    print("++++++++++++++++++++", access)
    cursor.execute(
        "select * from emeet_company where `id` in (select `company_id` from emeet_forums where `fid` in (" + access + "))")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        for a in userlist:
            str1 += a[2] + "|"
        str1 = str1[:-1]
    return str1


@csrf_exempt
def notes_upload2_new_enc(request):
    try:
        json2 = request.POST.get('json')
        jsonn = ""
        userid = ""
        Deviceid = ""
        token = ""
        if json2 == "" or not json2:
            json2 = object.decryptString(request.form['json'])
        else:
            json2 = object.decryptString(request.POST.get('json'))
        print(json2)
        json2 = json.loads(json2)
        jsonn = json2['notes']
        userid = json2['userid']
        Deviceid = json2['Deviceid']
        token = json2['token']
        res = {}
        dtres = {}
        if Deviceid == "" or not Deviceid:
            Deviceid = "12345"
        try:
            if token and token != "":
                userid1 = token.split('_')
                cursor = connection.cursor()
                cursor.execute(
                    "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
                userlist = cursor.fetchall()
                if len(userlist) > 0:
                    N = json.loads(jsonn)
                    print(N)
                    notes = N['notings']
                    for a in notes:
                        insert_update(a, userid, Deviceid)

                        # if not result:
                        #     res['status'] = "false"
                        #     dtres['response'] = 'false'
                        # else:
                        #     res['status'] = "true"
                        #     dtres['response'] = 'true'

                    res['status'] = "true"
                    dtres['token'] = userlist[0][0]
                    dtres['response'] = 'true'
                else:
                    dtres['response'] = 'false'
                    res['status'] = 'false'

            else:
                dtres['response'] = '<error>Invalid parameters</error>'
                res['status'] = 'false'

        except:
            traceback.print_exc()
            dtres['response'] = traceback.format_exc()
            res['status'] = 'false'
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)
    except:
        traceback.print_exc()
        dtres['response'] = "<error>Invalid Parameters</error>"
        res['status'] = 'false'
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)


@csrf_exempt
def ret_approvals(request):
    # status = request.GET.get('status')
    # userid = request.GET.get('userid')
    status = request.POST.get('status')
    userid = request.POST.get('userid')
    cursor = connection.cursor()
    print('ret apprv sts---->', status)
    print('ret apprv userid---->', userid)
    if not status:
        status = "mn"
    if not userid:
        userid = request.Form["userid"];
    if status == "A":

        cursor.execute(
            "select a.id,a.title,a.filename,a.company,b.action,a.expiry_dt,c.fname from emeet_approvals a left join emeet_approval_users b on a.id=b.id left join emeet_forums c on c.fid = a.company where b.userid = '" + userid + "' and(b.action = 'Approved' or b.action = 'Rejected' or b.action = 'Abstained' or b.action = 'Abstain')order by a.Id desc limit 10")
        userlist = cursor.fetchall()
    else:
        cursor.execute(
            "select a.id,a.title,a.filename,a.company,b.action, a.expiry_dt , c.fname from emeet_approvals a left join emeet_approval_users b on a.id=b.id left join emeet_forums c on c.fid = a.company where b.userid = '" + userid + "' and b.action = 'Pending' order by a.Id desc")
        userlist = cursor.fetchall()
    print("appr userlist--->", userlist)
    jsonn = "["

    if len(userlist) > 0:
        for a in userlist:
            fname = a[6]
            if not fname or fname == "":
                fname = 'generic'
            expry = a[5]
            if not expry:
                expry = ""
            else:
                expry = expry.strftime("%d/%m/%Y %H:%M:%S")
            jsonn += "{"
            jsonn += "\"id\":\"" + str(a[0]) + "\","
            jsonn += "\"title\":\"" + a[1] + "\","
            jsonn += "\"filename\":\"" + getLink(a[3], a[2]) + "\","
            jsonn += "\"status\":\"" + str(a[4]) + "\","
            jsonn += "\"CommitteeID\":\"" + str(a[3]) + "\","
            jsonn += "\"CommitteeName\":\"" + fname + "\","
            jsonn += "\"expiry_dt\":\"" + expry + "\""
            jsonn += "}"
            jsonn += ","
        jsonn = jsonn[:-1]
        print("jsson--->", jsonn)

    jsonn += "]"
    print("jsson11--->", jsonn)
    return HttpResponse(jsonn)


def getLink(Company, file):
    if Company.lower() == 'generic':
        return base11 + baseURL + 'static/approvals/' + file
    else:
        print("apprv url--->", baseURL + 'static/approvals/' + Company + "/" + file)
        return base11 + baseURL + 'static/approvals/' + Company + "/" + file


def insert_update(N, userid, deviceid):
    cursor = connection.cursor()
    cursor.execute("select count(*) from emeet_noting where userid='" + userid + "' and uniqId='" + N['uniqId'] + "'")
    userlist = cursor.fetchall()
    count = userlist[0][0]
    print("count---->", count)
    flag = N['updateFlag']
    res = -10
    if count > 0:
        cursor = connection.cursor()
        userlist1 = cursor.execute(
            "update emeet_noting set text='" + N['text'] + "',point1='" + N['point1'] + "',point2='" + N[
                'point2'] + "',modDate='" + formatDate(N['modDate']) + "',Flag='" + flag + "',page='" + N[
                'page'] + "',ag_id='" + N['ag_id'] + "',level='" + N['level'] + "',publicflag='" + N[
                'publicflag'] + "' where userid='" + userid + "' and uniqId='" + N['uniqId'] + "'")

        print("++++++++++++++++++++", userlist1)
    else:
        print("++++++++++++++  insert  +++++++++++++++++")
        q2 = "select mid from emeet_level0 where ag_id='" + N['ag_id'] + "'"

        if N['level'] == '0':
            q2 = "select mid from emeet_level0 where ag_id='" + N['ag_id'] + "'"
        elif N['level'] == "1":
            q2 = "select mid from emeet_level0  where ag_id =(select parent from emeet_level1 where ag_id ='" + N[
                'ag_id'] + "')";
        else:
            q2 = "select mid from emeet_level0  where ag_id =(select parent from emeet_level1 where ag_id  =(select parent from emeet_level2 where ag_id ='" + \
                 N['ag_id'] + "'))";

        cursor.execute(q2)
        userlist1 = cursor.fetchall()
        print("insert userlist1-->", userlist1)
        if len(userlist1) > 0:
            mid = userlist1[0][0]
            print("insert mid--->", mid)
            query = "insert into emeet_noting (userid,uniqId,text,point1,point2,modDate,Flag,deviceid,page,ag_id,level,mid,publicflag) values('" + userid + "','" + \
                    N['uniqId'] + "','" + N['text'] + "','" + N['point1'] + "','" + N['point2'] + "','" + formatDate(
                N['modDate']) + "','" + flag + "','" + deviceid + "','" + N['page'] + "','" + N['ag_id'] + "','" + N[
                        'level'] + "','" + str(mid) + "','" + N['publicflag'] + "')"
            print("insert auery-->", query)
            userlist1 = cursor.execute(query)

        else:
            print("mid not found")
    # if userlist1 != 1:
    #     return False
    # else:
    #     return True


def formatDate(date):
    d = datetime.datetime.strptime(date, '%Y%m%d%H%M%S%f')
    return d.strftime("%Y/%m/%d %H:%M:%S.%f %t")


def Escapestring(xmlstr):
    xmlstr = xmlstr.replace("''", "'");
    return xmlstr.replace('&', '&amp;')


def BxmlstrLevel1(id, fid, mainid, srno, condition):
    cursor = connection.cursor()
    cursor.execute(
        "select main.*,(case when code.name = '0' or code.name is null then '' else code.name end) as cname,(case when code.colorcode = '0' or code.colorcode is null then '' else code.colorcode end) as colorcode from emeet_level1 main left join emeet_agcolorcodes code on main.ColorId = code.id where parent = '" + str(
            id) + "' order by aid")
    userlist = cursor.fetchall()
    xmlstr1 = ""
    for a in userlist:
        parent_srno = srno + "." + excapseStr(getalphaID(a[6]))
        if condition:
            xmlstr1 += "<sagenda name=\"" + excapseStr(getalphaID(a[6])) + ") " + excapseStr(a[1]) + "\" pdf=\"" + a[
                4] + "\" url=\"" + getURL(fid, mainid, a[4]) + "\" level=\"1\" desc=\"" + excapseStr(
                a[2]) + "\" id=\"" + excapseStr(a[0]) + "\" v=\"" + excapseStr(
                a[5]) + "\" srno=\"" + srno + "\" colorname=\"" + excapseStr(a[8]) + "\" colorcode=\"" + excapseStr(
                a[9]) + "\">"
        else:
            xmlstr1 += "<sagenda name=\"" + excapseStr(getalphaID(a[6])) + ") " + excapseStr(
                a[1]) + "\" pdf=\"\" url=\"\" level=\"1\" desc=\"" + excapseStr(a[2]) + "\" id=\"" + excapseStr(
                a[0]) + "\" v=\"" + excapseStr(a[5]) + "\" srno=\"" + srno + "\" colorname=\"" + excapseStr(
                a[8]) + "\" colorcode=\"" + excapseStr(a[9]) + "\">"
        if hasChild(a[0], "2"):
            xmlstr1 += BxmlstrLevel2(a[0], id, fid, mainid, parent_srno, condition)
        xmlstr1 += "</sagenda>"
    return xmlstr1


def BxmlstrLevel2(id, ids, fid, mainid, parent_srno, condition):
    cursor = connection.cursor()
    cursor.execute(
        "select main.*,(case when code.name = '0' or code.name is null then '' else code.name end) as cname,(case when code.colorcode = '0' or code.colorcode is null then '' else code.colorcode end) as colorcode from emeet_level2 main left join emeet_agcolorcodes code on main.ColorId = code.id where parent = '" + str(
            id) + "' order by aid")
    userlist = cursor.fetchall()
    xmlstr1 = ""
    for a in userlist:
        val = a[6]
        rom = intToRoman(int(val))

        xmlstr1 += "<ssagenda name=\"(" + rom.lower() + ") " + a[1] + "\" "
        if condition:
            xmlstr1 += "pdf=\"" + a[4] + "\" "
            xmlstr1 += "url=\"" + getURL(fid, mainid, a[4]) + "\" level=\"2\" "
        else:
            xmlstr1 += "pdf=\"\" "
            xmlstr1 += "url=\"\" level=\"2\" "
        xmlstr1 += "colorname=\"" + a[8] + "\" "
        xmlstr1 += "colorcode=\"" + a[9] + "\" "
        xmlstr1 += "desc=\"" + str(a[2]) + "\" id=\"" + str(a[0]) + "\" v=\"" + str(a[5]) + "\" srno=\"" + str(
            parent_srno) + "\">"
        xmlstr1 += "</ssagenda>"
    return xmlstr1


def xmlstrLevel1(id, fid, mid):
    cursor = connection.cursor()
    cursor.execute("select * from emeet_level1 where parent='" + str(id) + "' order by ag_id")
    userlist = cursor.fetchall()
    xmlstr1 = ""
    if len(userlist) > 0:
        for a in userlist:
            strr = isExist(a[4], mid)
            if strr != "" or strr:
                xmlstr1 += strr + ","
            if hasChild(a[0], "2"):
                xmlstr1 += xmlstrLevel2(a[0], fid, mid)
    return xmlstr1


def xmlstrLevel2(id, fid, mid):
    cursor = connection.cursor()
    cursor.execute("select * from emeet_level2 where parent='" + str(id) + "' order by ag_id")
    userlist = cursor.fetchall()
    xmlstr2 = ""
    if len(userlist) > 0:
        for a in userlist:
            strr = isExist(a[4], mid)
            if strr != "" or strr:
                xmlstr2 += strr + ","

    return xmlstr2


def hasChild(a, level):
    cursor = connection.cursor()
    cursor.execute("select * from emeet_level" + str(level) + " where parent='" + str(a) + "'")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        return True
    else:
        return False


def isExist(doc, mid):
    fid = getFID(mid)
    path = basepath + "static/resources/" + getFname(str(fid)) + "/" + str(mid) + "/" + str(doc)
    if doc == "" or not doc:
        return ""
    else:
        return path


def getFID(mid):
    cursor = connection.cursor()
    cursor.execute("select fid from emeet_meeting where id='" + str(mid) + "'")
    userlist = cursor.fetchall()
    return userlist[0][0]


#
# def getLink1(t1, t2):
#     return "/Shared_Doc/" + str(t2) + "/" + str(t1)


def getabr(fid, flag):
    if fid != "" and fid:
        cursor = connection.cursor()
        commi = []
        cursor.execute(
            "select f.fname,c.abbr,c.name from emeet_forums f,emeet_company c where f.company_id=c.id and fid='" + str(
                fid) + "'")
        userlist = cursor.fetchall()
        if len(userlist) > 0:
            if flag == 'fname':
                return userlist[0][0]
            elif flag == 'companyname':
                return userlist[0][2]
            else:
                return userlist[0][1]
        else:
            return ""

    else:
        return ""


def getCommittees(access):
    cursor = connection.cursor()
    commi = []
    cursor.execute("select fid from emeet_forums where fid in (" + access + ") and stat='true' order by fid")
    userlist = cursor.fetchall()
    for a in userlist:
        commi.append(a[0])
    return commi


def no_days_pwd(userid):
    cursor = connection.cursor()

    cursor.execute("select pwd_dt from emeet_manageusers where `userid`='" + userid + "'")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        try:
            dt_Set = userlist[0][0]
            difference = (datetime.datetime.now() - dt_Set)
            print("))))))))))))))))))))))))))", difference.days)
            return difference.days
        except:
            return 0
    else:
        return 0


def getURL(fid, mid, filename):
    if filename and filename != "":
        # url = "http://127.0.0.1:8000/static/resources/" + getFname(str(fid)) + "/" + str(mid) + "/" + filename
        url = base11 + "/static/resources/" + getFname(str(fid)) + "/" + str(mid) + "/" + filename

        return url
    else:
        return ""


def getFname(fid):
    cursor = connection.cursor()
    cursor.execute("select fname from emeet_Forums where fid = '" + fid + "'")
    userlist = cursor.fetchall()
    return userlist[0][0]


def CurrentMeeting(fid):
    xml = ""

    cursor = connection.cursor()

    cursor.execute(
        "select dt,id,title from emeet_meeting where DATEDIFF(now(),dt)<=days and DATEDIFF(now(),dt)>=0 and `fid`='" + str(
            fid) + "' and status='true' order by dt")
    userlist = cursor.fetchall()

    if len(userlist) > 0:
        for a in userlist:
            xml += "<id title=\"" + str(a[2]) + "\" mid=\"" + str(a[1]) + "\" date=\"" + str(
                a[0].strftime("%m/%d/%Y %I:%M:%S %p")) + "\" status=\"0\" />"
    return xml


def PreviousMeeting(fid):
    xml = ""
    cursor = connection.cursor()

    cursor.execute(
        "select dt,id,title from emeet_meeting where date(DATE_ADD(dt, INTERVAL days DAY))<CURDATE() and `fid`='" + str(
            fid) + "' and status='true' order by dt desc limit 1")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        for a in userlist:
            xml += "<id title=\"" + str(a[2]) + "\" mid=\"" + str(a[1]) + "\" date=\"" + str(
                a[0].strftime("%m/%d/%Y %I:%M:%S %p")) + "\" status=\"1\" />"
    return xml


def generate_uuid():
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [8, 4, 4, 4, 12]
    for n in uuid_format:
        for i in range(0, n):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])

    return random_string


def getauthcode(access, status, lastlogin, wipe):
    if lastlogin and wipe == 0:
        print(lastlogin)
        if "." in str(lastlogin):
            lldate = datetime.datetime.strptime(str(lastlogin), "%Y-%m-%d  %H:%M:%S.%f")
        else:
            lldate = datetime.datetime.strptime(str(lastlogin), "%Y-%m-%d  %H:%M:%S")

        print(lldate)
        difference = datetime.datetime.now() - lldate
        print(difference.days)
        if difference.days > 30:
            return "7"
        else:
            if access == "0" or access == "" or not access:
                return "3"
            else:
                if status.lower() == "true":
                    return "1"
                else:
                    return "3"

    else:
        if not wipe:
            if access == "0" or access == "" or not access:
                return "3"
            else:
                if status == "true":
                    return "1"
                else:
                    return "3"
        else:
            return "8"


def excapseStr(xml):
    xml = str(xml)
    xml = xml.replace("''", "'");
    xml = xml.replace("\"", "&quot;");
    xml = xml.replace("<", "&lt;");
    xml = xml.replace(">", "&gt;");
    return xml.replace("&", "&amp;");


def UNsucess_login(userid):
    try:
        counter = 0
        cursor = connection.cursor()
        cursor.execute(
            "select *,TIMESTAMPDIFF(MINUTE,LUA,now()) as diff from emeet_manageusers where userid='" + userid + "' and active='True'")
        userlist = cursor.fetchall()
        userlist = list(userlist[0])
        if len(userlist) > 0:
            diff_count = userlist[30]
            if userlist[23]:
                dd = userlist[23]
            else:
                dd = "0"
            if int(dd) < 5:
                counter = int(dd) + 1
                a = cursor.execute("update emeet_manageusers set `attemptcount`=" + str(
                    counter) + " , `LUA`=now() where `userid`='" + str(userid) + "'")
                return True
            else:
                if diff_count >= 5:
                    a = cursor.execute(
                        "update emeet_manageusers set `accountStatus`='True' where `userid`='" + userid + "'")
                    return True
                else:
                    a = cursor.execute(
                        "update emeet_manageusers set `accountStatus`='False' where `userid`='" + userid + "'")
                    return False
        else:
            return False
    except:

        traceback.print_exc()
        return False


def Sucess_login(userid):
    try:
        cursor = connection.cursor()
        a = cursor.execute(
            "update emeet_manageusers set `attemptcount`=0 , `LUA`=now() where `userid`='" + userid + "'")
        return True
    except:
        traceback.print_exc()
        return False


def getAccess(commitee, access):
    print("in getAccess")
    print(commitee)
    xml = ""
    cursor = connection.cursor()
    if access == "0":
        xml += "0"
    else:
        if access == "usrmanage" or access == "admin":
            cursor.execute(
                "select f.fid,Replace(f.fname,'emeet_',''),c.abbr from emeet_forums f,emeet_company c where f.company_id=c.id and f.stat='true' and f.approved='approved' order by f.fid")
            userlist = cursor.fetchall()
            userlist = list(userlist)
            for ele in userlist:
                xml += str(ele[1]) + ";" + str(ele[2]) + ";"
            xml = xml[:-1]
        else:
            cursor.execute(
                "select f.fid,Replace(f.fname,'emeet_','') as fname,c.abbr from emeet_forums f,emeet_company c where f.company_id=c.id and f.stat='true' and f.approved='approved' and fid in (" + commitee + ") order by f.fid")
            userlist = cursor.fetchall()
            userlist = list(userlist)
            if len(userlist) > 0:
                for ele in userlist:
                    xml += str(ele[1]) + " " + str(ele[2]) + ";" + str(ele[0]) + ";"
                xml = xml[:-1]
    xml += ""
    return xml


# def get_presenter(userid):
#     cursor = connection.cursor()
#     cursor.execute("select * from emeet_forums where presentor = '" + userid + "'")
#     userlist = cursor.fetchall()
#     presentor = ""
#     if len(userlist) > 0:
#         for a in userlist:
#             presentor += userlist[0][0] + ","
#         presentor = presentor[:-1]
#     return presentor


def company(access):
    str1 = ""
    cursor = connection.cursor()
    print("++++++++++++++++++++", access)
    cursor.execute(
        "select * from emeet_company where `id` in (select `company_id` from emeet_forums where `fid` in (" + access + "))")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        for a in userlist:
            str1 += a[2] + "|"
        str1 = str1[:-1]
    return str1


@csrf_exempt
def ret_comments(request):
    mid = request.POST.get('momid')
    token = request.POST.get('token')
    userid = ""
    if mid == "" or not mid:
        userid = object.decryptString(request.form['userid'])

        mid = object.decryptString(request.form['momid'])

        token = object.decryptString(request.form['token'])
    else:
        userid = object.decryptString(request.POST.get('userid'))

        mid = object.decryptString(request.POST.get('momid'))

        token = object.decryptString(request.POST.get('token'))

    res = {}
    dtres = {}
    comments = []
    if token and token != "":

        cursor = connection.cursor()
        cursor.execute(
            "select token from emeet_manageusers where userid='" + userid + "' and token='" + token + "'")
        userlist = cursor.fetchall()
        if len(userlist) > 0:
            cursor.execute("select * from emeet_mom_comment where momid='" + str(
                mid) + "' and senderid='" + userid + "' order by dt desc")
            userlist1 = cursor.fetchall()
            print("comments---->", userlist1)
            if len(userlist1) > 0:
                for a in userlist1:
                    mobj = {}
                    try:
                        mobj['Comment'] = (base64.b64decode(a[2])).decode("utf-8")
                        print('enc comment--->', mobj['Comment'], type(mobj['Comment']))
                    except:
                        mobj['Comment'] = a[2]
                    mobj['PageNo'] = a[7]
                    mobj['CommentID'] = a[0]
                    mobj['Date'] = a[3].strftime("%m/%d/%Y %I:%M:%S %p")
                    comments.append(mobj)
                dtres['response'] = comments
                res['status'] = 'true'
                dtres['token'] = userlist[0][0]
            else:
                dtres['response'] = comments
                res['status'] = 'true'
                dtres['token'] = ""
        else:
            dtres['response'] = '<error>Invalid parameters</error>'
            res['status'] = 'false'
            dtres['token'] = ""
    else:
        dtres['response'] = '<error>Invalid parameters</error>'
        res['status'] = 'false'
        dtres['token'] = ""
    # res['data'] = object.encryptString(dtres)

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    return JsonResponse(res)


# ___________________________________Ambika______________________________________________________________________________
@csrf_exempt
def ret_briefcase(request):
    query = request.POST.get('userid')
    userid = ""
    token = ""

    if query == "" or not query:
        userid = object.decryptString(request.form['userid'])
        token = object.decryptString(request.form['token'])
    else:
        userid = object.decryptString(request.POST.get('userid'))
        token = object.decryptString(request.POST.get('token'))

    res = {}
    dtres = {}

    if token and token != "":
        cursor = connection.cursor()
        cursor.execute("select * from emeet_manageusers where userid='" + userid + "' and token='" + token + "'")
        userlist = cursor.fetchall()
        list1 = []
        if len(userlist) > 0:
            cursor.execute("select * from emeet_briefcase where userid='" + userid + "'")
            userlist1 = cursor.fetchall()
            if len(userlist1) > 0:
                for u in userlist1:
                    mobj = {}
                    mobj['id'] = u[0]
                    mobj['userid'] = u[1]
                    mobj['module'] = u[2]
                    mobj['title'] = u[3]
                    mobj['filename'] = 'static/Briefcase/' + userid + "/" + u[4]
                    mobj['date'] = u[5].strftime("%d/%m/%Y %I:%M:%S %p")
                    list1.append(mobj)
            dtres['token'] = token
            dtres['response'] = json.dumps(list1)
            res['status'] = 'true'
        else:
            dtres['token'] = ""
            dtres['response'] = "Invalid token"
            res['status'] = "false"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response------------------->", res)
    return JsonResponse(res)


@csrf_exempt
def ret_addBriefcase(request):
    try:
        query = request.POST.get("userid")
        userid = ""
        token = ""
        module = ""
        title = ""
        filepath = ""
        filename = ""

        if query == "" or not query:
            userid = object.decryptString(request.form['userid'])
            token = object.decryptString(request.form['token'])
            module = object.decryptString(request.form['module'])
            title = object.decryptString(request.form['title'])
            filepath = object.decryptString(request.form['filepath'])
            filename = object.decryptString(request.form['filename'])
        else:
            userid = object.decryptString(request.POST.get('userid'))
            token = object.decryptString(request.POST.get('token'))
            module = object.decryptString(request.POST.get('module'))
            title = object.decryptString(request.POST.get('title'))
            filepath = object.decryptString(request.POST.get('filepath'))
            filename = object.decryptString(request.POST.get('filename'))

        res = {}
        dtres = {}

        if token and token != "":
            cursor = connection.cursor()
            cursor.execute("select * from emeet_manageusers where userid='" + userid + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            print("userlist---------->", userlist)
            for u in userlist:
                utoken = u[15]
            print("token fr==", utoken)
            if len(userlist) > 0:  # module, title, filepath, filename, userid
                print("filepath****", filepath)
                result = addFiles(module, title, (basepath + filepath), filename, userid)
                dtres['token'] = utoken
                if result:
                    dtres['response'] = "True"
                else:
                    dtres['response'] = "False"
                res['status'] = "true"
            else:
                dtres['token'] = ""
                dtres['response'] = "Invalid token"
                res['status'] = "false"

    except Exception as e:
        traceback.print_exc()
        res = {}
        dtres = {}
        dtres['token'] = ""
        dtres['response'] = "Error=" + str(e)
        res['status'] = "true"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response-------------------->", res)
    return JsonResponse(res)


def addFiles(module, title, filepath, filename, userid):
    try:
        fs = FileSystemStorage()
        if not os.path.exists(basepath + "static/Briefcase/" + userid):
            os.makedirs(basepath + "static/Briefcase/" + userid)

        currentdate = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        myPath = currentdate + "_" + module + "_" + title + "_" + filename
        print('--->', myPath)
        savePath = basepath + "static/Briefcase/" + userid + "/" + myPath
        print("====>", savePath)
        if not fs.exists(savePath):
            print("file p---->", filepath)
            # /emeeting_new/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/static/resources/Board Committee/1
            copyfile(filepath, savePath)
            print("## copied +++")
        cursor = connection.cursor()
        a = cursor.execute(
            "insert into emeet_briefcase (userid,module,title,filename,InsertDate) values ('" + userid + "','" + module + "','" + title + "','" + str(
                myPath) + "',now())")
        print("a===============>", a)
        if a == 1:
            return True
        else:
            return False
    except:
        traceback.print_exc()
        return False


@csrf_exempt
def ret_module_details(request):
    res = {}
    try:
        count = 0
        tdate = ""
        j = request.POST.get('json')
        print("request---------------------->", j, "\nlength--------->", len(j))
        if j == "" or not j:
            j = request.form['json']
        if j and j != "":
            j = json.loads(j)
            for key, val in j.items():
                if key == "LoginId":
                    userid = val
                if key == "modules":
                    modul = val
            print("userid-->", userid)
            print("modu--->", modul, "\nlength------->", len(modul))
            c = len(modul)
            for m in modul:
                print("m----->", m)
                if m['Eventname'] == "" or not m['Eventname']:
                    m['Eventname'] = "--"
                if m['Action'] == "" or not m['Action']:
                    m['Action'] = ""
                if m['Meeting_ID'] == "" or not m['Meeting_ID']:
                    m['Meeting_ID'] = ""
                if m['Agenda_ID'] == "" or not m['Agenda_ID']:
                    m['Agenda_ID'] = ""
                if m['Level'] == "" or not m['Level']:
                    m['Level'] = ""
                if m['Value'] == "" or not m['Value']:
                    m['Value'] = ""
                if m['Document_ID'] == "" or not m['Document_ID']:
                    m['Document_ID'] = ""
                if m['deviceInfo'] == "" or not m['deviceInfo']:
                    m['deviceInfo'] = ""
                if m['Date'] == "" or not m['Date']:
                    tdate = ""
                else:
                    tdate = datetime.datetime.strptime(m['Date'], "%d-%m-%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                cursor = connection.cursor()
                a = cursor.execute(
                    "Insert Into activity_logs_modules (UserID,EventName,Date,Action,Mid,aid,Level,Value,Document_ID,deviceInfo,InsertDateTime)" +
                    "values('" + userid + "','" + m['Eventname'] + "','" + tdate + "','" + m['Action'] + "','" + m[
                        'Meeting_ID'] + "','" + m['Agenda_ID'] + "','" + m['Level'] + "','" + m['Value'] + "','" + m[
                        'Document_ID'] + "','" + m['deviceInfo'] + "',now())")
                print("a------>", a)
                if a == 1:
                    count = count + 1
                    if count == c:
                        res['status'] = "true"
                else:
                    res['status'] = "Something Went Wrong"
        else:
            res = {"Status": "Failure", "Message": "Parameters are empty."}
    except:
        traceback.print_exc()

    print("resopnse------------>", res)
    return JsonResponse(res)


@csrf_exempt
def ret_add_comment(request):
    mid = request.POST.get('momid')
    token = request.POST.get('token')
    userid = ""
    comments = ""
    pageno = ""

    if mid == "" or not mid:
        mid = object.decryptString(request.form['momid'])
        token = object.decryptString(request.form['token'])
        userid = object.decryptString(request.form['userid'])
        comments = object.decryptString(request.form['comments'])
        pageno = object.decryptString(request.form['pageno'])
    else:
        mid = object.decryptString(request.POST.get('momid'))
        token = object.decryptString(request.POST.get('token'))
        userid = object.decryptString(request.POST.get('userid'))
        comments = object.decryptString(request.POST.get('comments'))
        pageno = object.decryptString(request.POST.get('pageno'))

    res = {}
    dtres = {}

    if token and token != "":
        cursor = connection.cursor()
        cursor.execute("select token from emeet_manageusers where userid='" + userid + "' and token='" + token + "'")
        userlist = cursor.fetchall()
        if len(userlist) > 0:
            cursor.execute("select * from emeet_mom1 where id='" + str(mid) + "'")
            userlist1 = cursor.fetchall()
            if len(userlist1) > 0:
                for u in userlist1:
                    filename = u[2]
                    title = u[8]
                a = cursor.execute(
                    "insert into emeet_mom_comment(momid,comment,dt,fileName,senderid,title,pageno) values('" + str(
                        mid) + "','" + str(getBase64EncodedString(
                        comments)) + "',now(),'" + filename + "','" + userid + "','" + title + "','" + str(
                        pageno) + "')")
                if a == 1:
                    dtres['token'] = token
                    dtres['response'] = "true"
                    res['status'] = "true"
                else:
                    dtres['token'] = ""
                    dtres['response'] = "<error>An error has occurred</error>"
                    res['status'] = "false"
            else:
                dtres['token'] = ""
                dtres['response'] = "<error>Invalid Parameters</error>"
                res['status'] = "false"
        else:
            dtres['token'] = ""
            dtres['response'] = "<error>Invalid Parameters</error>"
            res['status'] = "false"
    else:
        dtres['token'] = ""
        dtres['response'] = "<error>Invalid Parameters</error>"
        res['status'] = "false"

    # res['data'] = dtres
    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response------------------------>", res)
    return JsonResponse(res)


def getBase64EncodedString(input):
    bs = bytearray(input, encoding='utf-8')
    enc = base64.b64encode(bs).decode('utf-8')
    print("encoded---------->", enc)
    return enc


@csrf_exempt
def ret_mom_comment(request):
    cursor = connection.cursor()
    res = {}
    dtres = {}

    j = request.POST.get('json')
    if j == "" or not j:
        j = object.decryptString(request.form['json'])
    else:
        j = object.decryptString(j)

    j = json.loads(j)
    id = j['id']
    token = j['token']
    datalist = []
    if id and id != "":
        if token and token != "":
            userid1 = token.split("_")
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            if len(userlist) > 0:
                cursor.execute("select * from emeet_approval_users where id='" + str(
                    id) + "' and comments is not null order by dt desc")
                userlist1 = cursor.fetchall()

                if len(userlist1) > 0:
                    for u in userlist1:
                        mobj = {}
                        mobj['comment'] = u[4]
                        mobj['senderid'] = u[1]
                        mobj['sender_name'] = getuname(u[1])
                        mobj['status'] = u[2]
                        mobj['date'] = u[3].strftime("%m/%d/%Y %I:%M:%S %p")
                        datalist.append(mobj)
                dtres['token'] = userlist[0][0]
                dtres['response'] = datalist
                res['status'] = "true"
            else:
                dtres['token'] = ""
                dtres['response'] = "false"
                res['status'] = "false"
        else:
            dtres['token'] = ""
            dtres['response'] = "false"
            res['status'] = "false"
    else:
        dtres['token'] = ""
        dtres['response'] = "<error>Invalid Parameters</error>"
        res['status'] = "false"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    # res['data'] = dtres
    print("response---------------------------->", res)
    return JsonResponse(res)


def getuname(userid):
    cursor = connection.cursor()
    cursor.execute("select ename from emeet_manageusers where userid='" + userid + "'")
    userlist = cursor.fetchall()
    if len(userlist) > 0:
        return userlist[0][0]
    else:
        return ""


@csrf_exempt
def action_approval_enc(request):
    cursor = connection.cursor()
    res = {}
    dtres = {}
    try:
        j = request.POST.get('json')
        id = ""
        action = ""
        comments = ""
        userid = ""
        timeStamp = ""
        token = ""

        if j == "" or not j:
            j = object.decryptString(request.form['json'])
        else:
            j = object.decryptString(j)

        j = json.loads(j)
        id = j['id']
        action = j['action']
        comments = j['comments']
        userid = j['userid']

        if "token" in j.keys():
            token = j['token']
        else:
            token = ""

        if "timeStamp" in j.keys():
            timeStamp = j['timeStamp']
        else:
            timeStamp = ""

        if token and token != "":
            userid1 = token.split("_")
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            if len(userlist) > 0:
                cursor.execute("select count(*) from emeet_approvals where id='" + str(id) + "'")
                userlist1 = cursor.fetchall()
                print("userlist1====>", userlist1[0][0])
                if userlist1[0][0] > 0:
                    res1 = 0
                    if action and action != "":
                        res1 = cursor.execute(
                            "update emeet_approval_users set action='" + action + "',dt=now(),comments='" + comments + "' where id='" + str(
                                id) + "' and userid='" + userid + "'")
                        print("res1--------->", res1)
                        r = SendMail_approval(userid, id)
                        print("r---->", r)
                    if res1 == 1:
                        dtres['token'] = userlist[0][0]
                        dtres['response'] = "true"
                        res['status'] = "true"
                        checkApprovalstatus(id)
                    else:
                        dtres['response'] = "false"
                        res['status'] = "false"
                else:
                    dtres['response'] = "Invalid ID"
                    res['status'] = "false"

            else:
                dtres['response'] = "false"
                res['status'] = "false"
        else:
            dtres['response'] = "<error>Invalid Parameters</error>"
            res['status'] = "false"
    except:
        traceback.print_exc()
        dtres['response'] = "false"
        res['status'] = "false"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    # res['data'] = dtres
    print("response---------------------->", res)
    return JsonResponse(res)


def SendMail_approval(userid, id):
    print("appr mail---->", userid, "---->", id)
    status = ""
    try:
        esub = "Reminder regarding voting resolution"

        cursor = connection.cursor()
        cursor.execute(
            "select userid from emeet_approval_users where userid!='" + userid + "' and id='" + str(id) + "'")
        userlist = cursor.fetchall()
        print("userlist-------->", userlist)

        for uname in userlist:
            print("uname------>", uname[0])
            ebody = "Dear " + uname[
                0].capitalize() + ",<br><br>" + "This is to inform to you that " + userid.capitalize() + " user has marked his vote on the voting resolution assigned to you.<br> Kindly mark your vote for the same through the application.<br><br><br> Regards, <br><br>Secretarial Team.<br><br>This is a system generated email, please do not reply to this email."

            cursor.execute("select email from emeet_manageusers where userid='" + uname[0] + "'")
            mailid = cursor.fetchall()
            email = [mailid[0][0]]
            print("email===>", email)
            me = ['ambika@mobitrail.com']
            send_multiemail(esub, ebody, me)
            # send_multiemail(esub, ebody, email)
        return "Success"

    except:
        traceback.print_exc()
        status = "Success1"
    return status


def checkApprovalstatus(id):
    cursor = connection.cursor()
    cursor.execute("select status from emeet_approvals where id='" + str(id) + "'")
    status = cursor.fetchall()
    print("status------------------>", status)
    if status[0][0] == 'Approved' or status[0][0] == 'Reject':
        print("done")
    else:
        cursor.execute(
            "select status_count from emeet_myapprovals_statuscount where id='" + str(id) + "' and action='Approved'")
        approval_count = cursor.fetchall()
        print("approval_count--------------->", approval_count)
        cursor.execute(
            "select status_count from emeet_myapprovals_statuscount where id='" + str(id) + "' and action='Rejected'")
        reject_count = cursor.fetchall()
        print("reject_count--------------->", reject_count)
        cursor.execute("select count(*) from emeet_approval_users where id='" + str(id) + "'")
        total_count = cursor.fetchall()
        print("total_count--------------->", total_count)

        if len(approval_count) == 0:
            approval_cnt = "0"
        else:
            approval_cnt = approval_count[0][0]

        if len(reject_count) == 0:
            reject_cnt = "0"
        else:
            reject_cnt = reject_count[0][0]

        if (float(approval_cnt) / float(total_count[0][0])) / 100 > 50.00:
            print("Approved+++++++++++++++++++++++++++")
            cursor.execute("select max(dt) from emeet_approval_users where id='" + str(id) + "' and action='Approved'")
            dt = cursor.fetchall()
            a = cursor.execute(
                "update emeet_approvals set status='Approved',last_update='" + str(dt[0][0]) + "' where id='" + str(
                    id) + "'")
            print("updated | a------------>", a)
        elif (float(reject_cnt) / float(total_count[0][0])) / 100 > 50.00:
            print("Rejected++++++++++++++++++++")
            cursor.execute("select max(dt) from emeet_approval_users where id='" + str(id) + "' and action='Rejected'")
            dt = cursor.fetchall()
            a = cursor.execute(
                "update emeet_approvals set status='Rejected',last_update='" + str(dt[0][0]) + "' where id='" + str(
                    id) + "'")
            print("updted | a ------------>", a)
        else:
            print("Pending++++++++++++++++++++++++")


@csrf_exempt
def sendPass_enc(request):
    try:
        j = request.POST.get('json')
        print("j--->", j)
        if j == "" or not j:
            j = request.form['json']
        email = ""
        message = ""
        subject = ""
        userid = ""
        CC = ""

        j = object.decryptString(j)
        print("decrypt j====>", j)
        j = json.loads(j)
        email = j['email']
        message = j['msg']
        subject = j['subject']

        res = {}
        dtres = {}

        if "token" in j.keys():
            print("present | value==>", j['token'])
            dtres['token'] = j['token']
        else:
            print("not present")
            dtres['token'] = ""

        if "userid" in j.keys():
            userid = j['userid']
        else:
            userid = ""
        print("userid--->", userid, "len==", len(userid))

        cursor = connection.cursor()
        if userid != "" or len(userid) != 0:
            print("userid not null")
            if email == "":
                email = getEmail(userid)
            if CheckMailCount(userid):
                print("CheckMAilCount+++++++++++++++++++++++++++++++++++++++")
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                a = cursor.execute(
                    "Insert into emeet_retsetpwd_status (userid,status,dt) values('" + userid + "','0',now())")
                cursor.execute("select id from emeet_retsetpwd_status where userid='" + userid + "' order by id desc")
                ulist = cursor.fetchall()
                ResetID = ulist[0][0]
                print("resetid--->", ResetID)

                message = "Dear " + getInfo(
                    userid) + ",<br /><br />" + "Please click on the below link to re-set your password.<br /><br />" + CreateLink1(
                    userid,
                    ResetID) + "<br /><br /> Regards,\n\n<br /><br /> Secretarial Team. <br /><br /> This is a system generated email,please do not reply to this email."

                # message = "Dear " + getInfo(
                #     userid) + ",\n\n" + "Please click on the below link to re-set your password.\n\n" + CreateLink1(
                #     userid,
                #     ResetID) + "\n\n Regards,\n\n\n\n Secretarial Team. \n\n This is a system generated email,please do not reply to this email."
                mailstr = SendMail(email, message, "Reset Password for Meeting Manager Application", True, CC)
                res['status'] = 'true'

                if mailstr == 'true':
                    cursor.execute(
                        "select case when PwdResetMailCount is null then 0 else PwdResetMailCount end as PwdResetMailCount from emeet_manageusers where userid='" + userid + "'")
                    ulist = cursor.fetchall()
                    count = ulist[0][0] + 1
                    a = cursor.execute(
                        "update emeet_manageusers set PwdResetMailCount='" + str(
                            count) + "' where userid='" + userid + "'")
                    activity = "iPad : Password Reset requested for  " + userid
                    query = "insert into `emeet_cmslogs` (`activity`,`type`,`userid`) values('" + activity + "','iPad','" + userid + "')"
                    print(query)
                    cursor.execute(query)

                    dtres['response'] = 'true'
                else:
                    dtres['response'] = 'false'
            else:
                res['status'] = 'true'
                dtres['response'] = 'Please try after 5 minutes.'
        else:
            if ";" in email:
                CC = email[email.index(';') + 1]
                email = email[0, email.index(';')]
            print("cc==============>", CC)
            res['status'] = 'true'
            dtres['response'] = SendMail(email, message, subject, False, CC)
            cursor.execute("select userid from emeet_manageusers where email='" + email + "'")
            ulist = cursor.fetchall()
            activity = "iPad : Send Notes to " + ulist[0][0]
            query = "insert into `emeet_cmslogs` (`activity`,`type`,`userid`) values('" + activity + "','iPad','" + \
                    ulist[0][0] + "')"
            print(query)
            cursor.execute(query)

        # res['data'] = dtres

        sdtres = json.dumps(dtres, separators=(',', ':'))
        print("sdtres---->", sdtres)
        res['data'] = object.encryptString(sdtres)
        print("response---------------------->", res)
        return JsonResponse(res)
    except:
        return HttpResponse(traceback.format_exc())


def CreateLink1(userid, ResetID):
    dt = datetime.datetime.now()
    print("dt----->", dt)
    plaintext = str(dt).encode("utf-8")
    enc_dt = encryption(plaintext)
    dt_ciphertext = enc_dt.decode("utf-8")

    print("resetid--->", ResetID)
    plaintext = str(ResetID).encode("utf-8")
    enc_resetid = encryption(plaintext)
    resetid_ciphertext = enc_resetid.decode("utf-8")

    uid = hashlib.md5(userid.encode()).hexdigest().upper()
    print("uid--->", uid)

    url = base11 + baseURL +"resetPassword?mob=1&v=" + uid + "," + dt_ciphertext + "," + resetid_ciphertext
    # url = baseURL + "reset_pwd_ipad?mob=1&v=" + uid + "," + dt_ciphertext + "," + resetid_ciphertext
    return "Click <a href='" + url + "'>Here</a> to Reset"


def SendMail(email, message, sub, flag, cc):
    try:
        email = 'ambika@mobitrail.com'
        ob = s.SMTP("smtp.gmail.com", 587)
        ob.starttls()
        ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
        msg = MIMEMultipart('alternative')
        msg['From'] = 'mobitrail.technology@gmail.com'
        # msg['To'] = email
        # msg['Cc'] = cc
        msg['To'] = 'ambika@mobitrail.com'

        msg['Subject'] = sub
        if flag:
            html = message
            part1 = MIMEText(html, 'html')
            msg.attach(part1)
        else:
            part2 = MIMEText(message)
            msg.attach(part2)

        print(msg.as_string())

        ob.sendmail('mobitrail.technology@gmail.com', email, msg.as_string())
        print("successsful")
        status = "true"
        ob.quit()
    except Exception as e:
        print("Err: ", e)
        status = "false"
    return status


def getEmail(userid):
    cursor = connection.cursor()
    cursor.execute("select email from emeet_manageusers where userid='" + userid + "'")
    emaillist = cursor.fetchall()
    if len(emaillist) > 0:
        return emaillist[0][0]
    else:
        return ""


def CheckMailCount(userid):
    cursor = connection.cursor()
    cursor.execute(
        "select case when PwdResetMailCount is null then 0 else PwdResetMailCount end as PwdResetMailCount from emeet_manageusers where userid='" + userid + "'")
    res = cursor.fetchall()
    mailcount = res[0][0]
    print("mailcount====>", mailcount)
    if mailcount >= 2:
        cursor.execute(
            "select * from emeet_retsetpwd_status where userid='" + userid + "' order by dt desc limit 2")
        userlist = cursor.fetchall()
        dt = ''
        li = []
        for user in userlist:
            dt = user[3].strftime('%Y-%m-%d %H:%M:%S')
            li.append(dt)
            status = user[2]
            li.append(status)
        print("li====>", li)
        current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("type--->", type(current), " | ", type(dt))
        ts = datetime.datetime.strptime(current, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(li[0],
                                                                                                   "%Y-%m-%d %H:%M:%S")

        print("ts==>", ts, " | ", type(ts))
        days, seconds = ts.days, ts.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        print("tsmin------------>", minutes)
        if li[1] == "True" or li[3] == "True":
            a = cursor.execute("update emeet_manageusers set PwdResetMailCount='0' where userid='" + userid + "'")
            if a == 1:
                return True
        else:
            if minutes > 5:
                a = cursor.execute(
                    "update emeet_manageusers set PwdResetMailCount='0' where userid='" + userid + "'")
                if a == 1:
                    return True
            else:
                return False
    else:
        return True


def getInfo(userid):
    cursor = connection.cursor()
    cursor.execute("select ename from emeet_manageusers where userid='" + userid + "'")
    res = cursor.fetchall()
    return res[0][0]


@csrf_exempt
def new_pass_enc(request):
    cursor = connection.cursor()
    try:
        j = request.POST.get('json')
        qu = ""
        ans = ""
        uname = ""
        password = ""
        token = ""

        if j == "" or not j:
            j = object.decryptString(request.form['json'])
        else:
            j = object.decryptString(j)

        j = json.loads(j)
        qu = j['que']
        ans = j['ans']
        uname = j['name']
        password = j['pass']
        token = j['token']

        res = {}
        dtres = {}

        if token != "" or not token:
            userid = token.split('_')
            print("userid=======>", userid)
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()

            if len(userlist) > 0:
                res['status'] = 'true'
                dtres['token'] = userlist[0][0]
                dtres['response'] = checkpwd(password, qu, ans, uname)

            else:
                res['status'] = 'false'
                dtres['token'] = ""
                dtres['response'] = "Invalid token"
        else:
            print("else============")
            res['status'] = 'false'
            dtres['token'] = ""
            dtres['response'] = "Invalid parameters"

        sdtres = json.dumps(dtres, separators=(',', ':'))
        res['data'] = object.encryptString(sdtres)
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()


todaypass = True
usr = ""
errorMsg = "You can not use old password"


def checkpwd(password, qu, ans, uname):
    if len(password) >= 8:
        # request.session['uname'] = uname
        checkPassword(uname, password)
        if todaypass:
            plaintext = password.encode("utf-8")
            enc_pass = encryption(plaintext)
            ciphertext = enc_pass.decode("utf-8")
            print("ciphertext----------->", ciphertext)

            cursor = connection.cursor()
            a = cursor.execute(
                "Update emeet_manageusers set pwd='" + ciphertext + "',pwd_dt=now(),que='" + qu + "',ans='" + ans + "' where userid='" + uname + "'")
            print("a====>", a)
            if a == 1:
                return "true"
            else:
                return "false"
        else:
            return errorMsg
    else:
        return "Password should contain minimum 8 characters"


def checkPassword(uname, password):
    try:
        check = ""
        cursor = connection.cursor()
        cursor.execute("select id,(pass) from emeet_pwdhist where userid='" + uname + "' order by id")
        userlist = cursor.fetchall()
        print("length------->", len(userlist))
        symbols = '!@#$%^&*?_~-Ã‚Â£()'
        if len(password) >= 8:
            if any(c.isdigit() for c in password) and any(c.isupper() for c in password) and any(
                    c.islower() for c in password) and any(c in symbols for c in password):
                print('good password')
                if len(userlist) >= 5:
                    print("userlist--->", userlist)
                    for user in userlist:
                        a = cursor.execute("delete from emeet_pwdhist where id='" + user[0] + "'")
                        print("a----->", a)
                if len(userlist) == 0:
                    check = True
                    todaypass = True
                else:
                    for user in userlist:
                        new = password
                        old = user[1]
                        pwd = old.encode('utf-8')
                        print("decry pass--->", decryption(pwd))
                        if password == decryption(pwd):
                            check = False
                            errorMsg = "Please use another password, you cannot use your last 5 used password"
                            todaypass = False
                            break
                        else:
                            check = True
                if check:
                    plaintext = password.encode("utf-8")
                    enc_pass = encryption(plaintext)
                    ciphertext = enc_pass.decode("utf-8")
                    print("### ciphertext ----------->", ciphertext)
                    a = cursor.execute(
                        "insert into emeet_pwdhist (userid,pass,pass_date) values ('" + uname + "','" + ciphertext + "',now())")
                    print("# inserted into emeet_pwdhist | a ----------------->", a)
            else:
                print('bad password')
                errorMsg = "Password must include a UpperCase alphabet,Lowercase alphabet,one numbers and symbol"
                todaypass = False
        else:
            errorMsg = "Password should contain minimum 8 characters"
            todaypass = False
    except:
        traceback.print_exc()


# ____________________________________________Vedanti __________________________________________________________________
# def getDate():
#     date1 = date.strftime("%m/%d/%Y %H:%M:%S %p")
#     print('date1 >>> ',date1)
#     return date1


@csrf_exempt
def ret_mom_details(request):
    cursor = connection.cursor()
    try:
        token = request.POST.get('token')
        fid = request.POST.get('fid')

        if token == "" or not token:
            token = object.decryptString(request.form['token'])
        else:
            token = object.decryptString(token)

        if fid == "" or not fid:
            fid = object.decryptString(request.form['fid'])
        else:
            fid = object.decryptString(fid)

        print('api fid---> ', fid)
        print('api token---> ', token)

        res = {}
        dtres = {}

        response_data = []

        if token != "" or not token:
            userid = token.split('_')
            print("userid=======>", userid)
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()

            if len(userlist) > 0:

                query = "Select *,(select title from emeet_meeting where id= em.mid and fid='" + str(
                    fid) + "') as Mtitle from emeet_mom1 em " \
                           "where em.mid in (Select distinct (mid) from emeet_mom1 where  fid='" + str(
                    fid) + "') and em.status=1";

                cursor.execute(query)
                print("----->",query)
                mom_details = cursor.fetchall()
                print('mom details-->  ', mom_details)

                for momdata in mom_details:
                    dt_dict = {}
                    query1 = "Select * from emeet_mapping_agenda where mom_id='" + str(momdata[0]) + "' and userid='" + \
                             userid[0] + "' and " \
                                         "approve_status='Pending'"
                    print(query1)
                    cursor.execute(query1)
                    momdata_details = cursor.fetchall()
                    print('momdata_details----> ', momdata_details)

                    if len(momdata_details) > 0:
                        dt_dict['mid'] = str(momdata[1])
                        dt_dict['title'] = momdata[12] + ' - ' + momdata[8]
                        dt_dict['mom'] = base11 + baseURL + 'static/resources/' + getFname(fid) + "/" + dt_dict[
                            'mid'] + "/" + momdata[2]
                        dt_dict['version'] = momdata[4]
                        dt_dict['momId'] = str(momdata[0])
                        momDate = momdata[6]
                        dt_dict['ExpiryDate'] = momDate.strftime("%m/%d/%Y %H:%M:%S")
                        # response_data.append(json.dumps(dt_dict))
                        response_data.append(dt_dict)
                    else:
                        pass

                print('res:\n', response_data)

                res['status'] = 'true'
                dtres['token'] = userlist[0][0]
                dtres['response'] = response_data

            else:
                res['status'] = 'false'
                dtres['token'] = ""
                dtres['response'] = "Invalid token"
        else:
            print("else============")
            res['status'] = 'false'
            dtres['token'] = ""
            dtres['response'] = "Invalid parameters"

        print("details json ---->\n", json.dumps(dtres, separators=(',', ':')))

        # res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        res['data'] = object.encryptString(str(dtres))
        print("response----------------------->", res)
        # res11 = object.decryptString(res['data'])
        # print(res11)

        return JsonResponse(res)
        # return HttpResponse(res)
    except:
        traceback.print_exc()


def getFname(fid):
    cursor = connection.cursor()
    cursor.execute("select fname from emeet_forums where fid=" + str(fid))
    forum = cursor.fetchall()
    return forum[0][0]


@csrf_exempt
def ret_mom_action(request):
    cursor = connection.cursor()
    try:
        jsonData = request.POST.get('json')

        id = ""
        action = ""
        comments = ""
        userid = ""
        token = ""

        if jsonData == "" or not jsonData:
            jsonData = object.decryptString(request.form['json'])
        else:
            jsonData = object.decryptString(jsonData)

        j = json.loads(jsonData)
        id = j['id']
        action = j['action']
        comments = j['comments']
        userid = j['userid']
        token = j['token']

        res = {}
        dtres = {}

        response_data = []

        if token != "" or not token:
            userid1 = token.split('_')
            print("userid=======>", userid1)
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()

            if len(userlist) > 0:
                query = "select count(*) from emeet_mom1 where id=" + str(id)
                cursor.execute(query)
                count = cursor.fetchall()[0][0]
                currentdate = datetime.datetime.now()
                if count > 0:
                    res_c = 5
                    if action != "" or not action:
                        query1 = "update `emeet_mapping_agenda` set approve_status='" + action + "',UpdateDateTime='" + str(
                            currentdate) + "'," \
                                           " comments='" + comments + "' where mom_id='" + str(
                            id) + "' and userid='" + userid + "' ";
                        cursor.execute(query1)
                        res_c = cursor.execute(query1)
                        print(res_c)
                        # r_mail = SendVotingResolutionMail(userid)

                    if res_c == 1:
                        res['status'] = 'true'
                        dtres['token'] = userlist[0][0]
                        dtres['response'] = 'true'
                    else:
                        res['status'] = 'false'
                        dtres['response'] = 'false'
                else:
                    res['status'] = 'false'
                    dtres['response'] = "Invalid ID"

            else:
                res['status'] = 'false'
                dtres['token'] = ""
                dtres['response'] = "Invalid token"
        else:
            print("else============")
            res['status'] = 'false'
            dtres['token'] = ""
            dtres['response'] = "Invalid parameters"

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()


def SendVotingResolutionMail(uname):
    cursor = connection.cursor()
    status = ''
    try:
        cursor.execute("select distinct userid from emeet_approval_users where userid!='" + uname + "' ");
        userlist = cursor.fetchall()
        print('----', userlist)

        for user in userlist:
            print(user)

            cursor.execute("select email from emeet_manageusers where userid=" + user[0])
            # email = cursor.fetchall()[0][0]

            ob = s.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
            subject = "Login Details for Emeeting Application"
            body = "Dear " + user[0] + ",<br><br>" + " This is to inform to you that " + uname + \
                   " user has marked his vote on the voting resolution assigned to you.<br>" + \
                   "Kindly mark your vote for the same through the application.<br><br><br>" + \
                   "Regards, <br><br>Secretarial Team.<br><br>This is a system generated email, please do not reply to this email.";

            message = "Subject:{}\n\n{}".format(subject, body)
            print(message)
            # ob.sendmail('mobitrail.technology@gmail.com', email, message)
            print("email sent successsfully !!!")
            ob.quit()

    except Exception as e:
        print("ex: ", e)


@csrf_exempt
def ret_sharedDoc(request):
    cursor = connection.cursor()
    try:
        token = ''
        userid = ''
        company_name = ''

        token = request.POST.get('token')
        userid = request.POST.get('userid')
        company_name = request.POST.get('company')

        if token == "" or not token:
            token = object.decryptString(request.form['token'])
        else:
            token = object.decryptString(token)

        if userid == "" or not userid:
            userid = object.decryptString(request.form['userid'])
        else:
            userid = object.decryptString(userid)

        if company_name == "" or not company_name:
            company_name = object.decryptString(request.form['company'])
        else:
            company_name = object.decryptString(company_name)

        print('api token---> ', token)
        print('api userid---> ', userid)
        print('api company---> ', company_name)

        res = {}
        dtres = {}
        #dt_dict = {}
        response_data = []

        if token != "" or not token:

            userid1 = token.split('_')
            print("userid1=======>", userid1)
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()

            if len(userlist) > 0:
                if company_name == "" or not company_name:
                    query = "select ms.id,ms.name,ms.link,ms.dt,ms.company,mc.name as company_name,mc.abbr " \
                            "from emeet_shareddoc ms,emeet_company mc where ms.company=mc.id and expiryDate > '" + getDate() + "' " \
                                                                                                                               "and ms.id in (select doc_id from emeet_document_users where userid='" + userid + "') order by ms.dt desc"
                    cursor.execute(query)
                    docs_data = cursor.fetchall()
                    print("docs data-----> ", docs_data)
                else:
                    query1 = "select ms.id,ms.name,ms.link,ms.dt,ms.company,mc.name as company_name,mc.abbr from" \
                             " emeet_shareddoc ms,emeet_company mc where ms.company=mc.id and expiryDate > '" + getDate() + "' " \
                                                                                                                            "and ms.id in (select doc_id from emeet_document_users where userid='" + userid + "') and " \
                                                                                                                                                                                                              "mc.abbr='" + company_name + "' order by ms.dt desc"
                    print(query1)
                    cursor.execute(query1)
                    docs_data1 = cursor.fetchall()
                    print("docs data1-----> ", docs_data1)

                    if len(docs_data1) > 0:
                        for dcData in docs_data1:
                            dt_dict = {}
                            print(dcData)
                            dt_dict['id'] = dcData[0]
                            dt_dict['name'] = dcData[1]
                            dt_dict['link'] = getLink1(dcData[2], dcData[4])
                            dt_dict['company'] = dcData[5]
                            dt_dict['company_abbr'] = dcData[6]
                            dt4 = dcData[3]
                            dt_dict['date'] = dt4.strftime("%m/%d/%Y %H:%M:%S")
                            response_data.append(dt_dict)
                        print('response data---->', response_data)

                    res['status'] = 'true'
                    dtres['token'] = userlist[0][0]
                    dtres['response'] = response_data

            else:
                res['status'] = 'false'
                dtres['token'] = ""
                dtres['response'] = "Invalid token"
        else:
            print("else============")
            res['status'] = 'false'
            dtres['token'] = ""
            dtres['response'] = "Invalid parameters"

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()


def getDate():
    currentdate = datetime.datetime.now()
    date1 = currentdate.strftime("%Y-%m-%d")
    date = date1 + " 00:00:00.000"
    # date = '2020-10-11 00:00:00.000'
    return date


def getLink1(link, company):
    reflink = "static/SharedDocs/" + company + "/" + link
    return reflink


@csrf_exempt
def ret_mail(request):
    cursor = connection.cursor()
    try:
        jsonData = request.POST.get('json')

        email = "";
        message = "";
        subject = "";
        userid = "";
        fid = "";
        mid = "";
        level = "";

        if jsonData == "" or not jsonData:
            jsonData = object.decryptString(request.form['json'])
        else:
            jsonData = object.decryptString(jsonData)

        j = json.loads(jsonData)
        email = j['email']
        message = j['msg']
        subject = j['subject']
        userid = j['userid']
        fid = j['fid']
        mid = j['mid']
        level = j['level']

        res = {}
        dtres = {}
        response_data = []

        if email != "" or not email:
            img_name = "";
            path = "";
            print("email found!!")
            if jsonData != "" or jsonData:
                print("json found!")
                imagedata = request.FILES.getlist('image')

                for imageFile in imagedata:
                    # print('img----> ',imageFile.name)
                    fs = FileSystemStorage()

                    date = datetime.datetime.now().strftime("%d%m%Y%H%M%S%p")
                    name = date + imageFile.name.replace(' ', '_').strip()
                    print('name----> ', name)
                    path = basepath + "static/Notes/" + name
                    img_name = name;
                    fs.save(path, imageFile)

            CC = "";
            email = "vedanti@mobitrail.com;ambika@mobitrail.com"
            if ';' in email:
                CC = email[email.index(";") + 1:]
                print('cc---> ', CC)
                email = email[0:email.index(";")]
                print('email--> ', email)

            query = "insert into emeet_mnotes_img(email,message,subject,userid,fid ,mid,level,image) " \
                    "values('" + email + "','" + message + "','" + subject + "','" + userid + "','" + str(
                fid) + "','" + str(mid) + "'," \
                                          "'" + str(level) + "','" + img_name + "')"
            # print(query)
            cursor.execute(query)
            response_data = SendAgendaSSMail(email, message, subject, 'false', img_name, CC);
            # activityLogs(request,"iPad : Add Note for Agenda"+ "iPad"+ userid);
            activity = "iPad : Add Note for Agenda"
            query = "insert into `emeet_cmslogs` (`activity`,`type`,`userid`) values('" + activity + "','iPad','" + userid + "')"
            print(query)
            cursor.execute(query)
            res['status'] = 'true'
            dtres['token'] = ''
            dtres['response'] = response_data


        else:
            print("else============")
            res['status'] = 'false'
            dtres['token'] = ""
            dtres['response'] = "Invalid parameters"

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()


def SendAgendaSSMail(email, message, subject, false, img_name, CC):
    status = "";
    email_list = []
    email_list.append(email)
    file_path = basepath + 'static/Notes/' + img_name
    print(basename(file_path))

    cc_email = CC.split(';')
    print(cc_email)
    email_list.extend(cc_email)
    print('email list--> ', email_list)

    try:
        ob = s.SMTP("smtp.gmail.com", 587)
        ob.starttls()
        ob.login('mobitrail.technology@gmail.com', 'mobitrail@1234')
        msg = MIMEMultipart('alternative')
        msg['From'] = 'mobitrail.technology@gmail.com'
        msg['To'] = email
        msg['Subject'] = subject
        msg['CC'] = ', '.join(cc_email)

        with open(file_path, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(file_path)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_path)
        msg.attach(part)

        # html = message.replace('\\n','<br>')
        # part1 = MIMEText(html, 'html')
        # msg.attach(part1)
        part2 = MIMEText(message)
        msg.attach(part2)

        print(msg.as_string())
        #
        ob.sendmail('mobitrail.technology@gmail.com', email_list, msg.as_string())
        status = 'true'
        print("successsful")
        ob.quit()

    except Exception as e:
        status = 'false'
        print("Err: ", e)
    return status


@csrf_exempt
def ret_board(request):
    company = request.POST.get('company')
    userid = request.POST.get('userid')
    cursor = connection.cursor()
    print('borad company---->', company)
    print('board userid---->', userid)

    if company == '' or company == None:
        company = request.Form['company']
    if company == '' or company == None:
        company = 'alpha'

    query = "Select * from emeet_board_members order by srno"
    cursor.execute(query)
    membersData = cursor.fetchall()
    print("member data---> ", membersData)

    strHtml = "<info>"

    for data in membersData:
        print("img--->",data[5],type(data[5]))
        img = excapseStr(data[5])
        if img == "" or not img:
            img = "def.jpg"
        descr = "Profile: " + data[3]
        strHtml += "<id name=\"" + excapseStr(data[1]) + "\" deg=\"" + excapseStr(
            data[2]) + "\" detail=\"" + excapseStr(descr) + "\" link=\"" + excapseStr(
            data[4]) + "\" image=\"" + base11 + "/static/resources/Board Members/" + img + "\" />"

    print("directors---->", strHtml)
    strHtml += "</info>";
    response = HttpResponse(content_type='text/xml')
    # Response.ContentType = "text/xml";
    response.write(strHtml);
    return response


def getDateUser(userid):
    response = HttpResponse(content_type='text/xml')
    cursor = connection.cursor()
    query = "select join_dt from emeet_manageusers where userid='" + userid + "' "
    cursor.execute(query)
    joinDate = cursor.fetchone()
    if len(joinDate) > 0:
        return "2000-01-01"
    else:
        response.write('hh')
        return datetime.now().strftime("%Y-%m-%d")


@csrf_exempt
def archive1_enc(request):
    cursor = connection.cursor()
    fid = request.POST.get('fid')
    print("fid----->", fid)
    maxid = ''
    userid = ''
    token = ''
    query = ''
    response = HttpResponse(content_type='text/xml')

    try:
        if fid == '' or not fid:
            fid = object.decryptString(request.form['fid'])
            maxid = request.Form['maxid']
            if not (maxid == '' or not maxid):
                maxid = object.decryptString(request.Form['maxid'])
            userid = object.decryptString(request.Form['userid'])
            token = object.decryptString(request.form['token'])
            print("in part--->", fid, maxid, userid)

        else:
            print("in else")
            fid = object.decryptString(request.POST.get('fid'))
            print("fid else--->", fid)
            maxid = request.POST.get('maxid')
            if not (maxid == '' or not maxid):
                maxid = object.decryptString(request.POST.get('maxid'))
            userid = object.decryptString(request.POST.get('userid'))
            token = object.decryptString(request.POST.get('token'))

            print("else part--->", fid, maxid, userid, token)

        join_dt = getDateUser(userid)
        print("join date---->", join_dt)
        dtres = {}
        resp = {}

        if token != '' or token:
            print("if token")
            if fid == '' or not fid:
                dtres['response'] = "Invalid parameters"
                resp['status'] = "false"
            else:
                print("fid found")
                useridtk = token.split('_')
                qtk = "select token from emeet_manageusers where userid='" + userid + "' and token='" + token + "'"
                cursor.execute(qtk)
                tokenData = cursor.fetchall()
                print("tokensss-->", tokenData)
                if len(tokenData) > 0:
                    result = ''
                    if maxid == None or maxid == '':
                        query = "select dt,id,title,mid from emeet_meeting where  fid=" + fid + " and cast(dt as Date) >'" + join_dt + "' and status='true' order by dt desc";
                        # cursor.execute(query)
                        # queryData = cursor.fetchall()
                        # print('queryData---->',queryData)
                    else:
                        query = "select dt,id,title,mid from emeet_meeting where  fid=" + fid + " and cast(dt as Date) >'" + join_dt + "' and status='true' and id > " + maxid + " order by dt desc";
                    print("qury---->>", query)
                    cursor.execute(query)
                    queryData = cursor.fetchall()
                    print('queryData---->', queryData)

                    if len(queryData) > 0:
                        for data in queryData:
                            result += "<id title=\"" + data[2] + "\" mid=\"" + data[3] + "\" date=\"" + (
                            data[0]).strftime("%m/%d/%Y %H:%M:%S %p") + "\" status=\"1\" />"
                    else:
                        result = ''
                    print("result--->", result)
                    res = ''
                    if result != None or result != '':
                        res = "<info>" + result + "</info>";
                    else:
                        res = "<info/>"

                    dtres['response'] = res
                    resp['status'] = 'true'
                    dtres['token'] = tokenData[0][0]



                else:
                    dtres['response'] = 'false'
                    resp['status'] = 'false'

        else:
            dtres['response'] = '<error>Invalid Parameters</error>'
            resp['status'] = 'false'

    except Exception as e:
        dtres = {}
        dtres['response'] = e
        resp['status'] = 'false'

    print("final dtres----->", dtres)

    # response = HttpResponse(content_type='text/json')
    #     # response.write(dtres)
    #     # return response

    resp['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    # res['data'] = dtres
    print("response----------------------->", resp)
    return JsonResponse(resp)


@csrf_exempt
def ret_aboutus_enc(request):
    cursor = connection.cursor()
    query = request.POST.get('userid')

    userid = ''
    token = ''

    try:
        if query == '' or not query:
            userid = object.decryptString(request.Form['userid'])
            token = object.decryptString(request.Form['token'])
        else:
            userid = object.decryptString(request.POST.get('userid'))
            token = object.decryptString(request.POST.get('token'))

        res = {}
        dtres = {}

        listData = []

        if token != '' or token:
            userid_ = token.split('_')
            cursor.execute("select token from emeet_manageusers where userid='" + userid + "'and token='" + token + "'")
            queryData = cursor.fetchall()
            print("querydata--> ", queryData)
            if len(queryData) > 0:
                if token != '' or token:
                    cursor.execute("select * from emeet_aboutus order by dt desc")
                    aboutUsData = cursor.fetchall()
                    if len(aboutUsData) > 0:

                        for data in aboutUsData:
                            dt_dict = {}
                            dt_dict['id'] = data[0]
                            dt_dict['name'] = data[1]
                            dt_dict['link'] = pdfurl + data[2]
                            dt_dict['dt'] = (data[3]).strftime("%d/%m/%Y %H:%M:%S")
                            listData.append(dt_dict)
                        print("listdata-----> ", listData)

                        dtres['response'] = listData
                        dtres['token'] = token
                        res['status'] = 'true'

                    else:
                        res['status'] = 'true'
                        dtres['response'] = ''
                        dtres['token'] = ''
                else:
                    dtres['response'] = " Invalid Parameters"
                    res['status'] = "false"
                    dtres['token'] = ''
            else:
                dtres['response'] = ''
                res['status'] = 'false'
                dtres['token'] = ''
        else:
            dtres['response'] = " Invalid Parameters"
            res['status'] = "false"
            dtres['token'] = ''

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()


def EscapeString(xmlstr):
    return xmlstr.replace("&", "&amp;")


@csrf_exempt
def calender_enc(request):
    cursor = connection.cursor()
    print("req---->  ", request)
    # id = request.GET.get("userid")
    # token = request.GET.get("token")
    # company = request.GET.get("company")
    id = request.POST.get("userid")
    token = request.POST.get("token")
    company = request.POST.get("company")
    startxml = "<info>"
    endxml = "</info>"
    xmlstr = ""
    print("----------->", id, token, company)
    if id == '' or not id:
        # token = object.decryptString(request.Form['token'])
        # id = object.decryptString(request.Form['userid'])
        # company = object.decryptString(request.Form['company'])
        # token = object.decryptString(request.GET.get('token'))
        # id = object.decryptString(request.GET.get('userid'))
        # company = object.decryptString(request.GET.get('company'))
        token = ''
        id = ''
        company = ''
    else:
        token = object.decryptString(request.POST.get('token'))
        id = object.decryptString(request.POST.get('userid'))
        company = object.decryptString(request.POST.get('company'))
    print("token--->", token)
    res = {}
    dtres = {}
    try:
        if token != '' or token:
            userid = token.split('_')
            cursor.execute("select token from emeet_manageusers where userid='" + id + "' and token='" + token + "' ")
            tokenList = cursor.fetchall()

            if len(tokenList) > 0:
                cursor.execute("Select committee from emeet_manageusers where userid='" + id + "' ")
                committeeData = cursor.fetchall()[0][0]
                committees = committeeData.split(',')
                print(committees)

                for fid in committees:
                    cursor.execute("select fname from emeet_forums where fid='" + fid + "' ")
                    fidData = cursor.fetchall()[0][0]

                    if True:
                        cursor.execute(
                            "select title,forum,venue,dt from emeet_annual_meetings where fid='" + fid + "' order by dt asc")
                        queryData = cursor.fetchall()
                        print("query data---> ", queryData,len(queryData))
                        if len(queryData) > 0:
                            try:
                                for data in queryData:
                                    #print("inner for")
                                    dateTimeObj = datetime.datetime.strptime(excapseStr(data[3]),'%d/%m/%Y %I:%M %p')
                                    #print("cal dt-->",dateTimeObj,type(dateTimeObj))
                                    calDate = dateTimeObj.strftime("%Y/%m/%d")
                                    calTime = dateTimeObj.strftime("%I:%M %p")
                                    forum = data[1]
                                    xmlstr += "<id title=\"" + excapseStr(data[0]) + "\" date=\"" + excapseStr(
                                        calDate) + "\" venue=\"" + excapseStr(
                                        data[2]) + "\" forum=\"" + excapseStr(forum) + "\" time=\"" + excapseStr(
                                        calTime) + "\"></id>"
                            except:
                                pass

                res['status'] = 'true'
                dtres['token'] = tokenList[0][0]
                xmlstr = EscapeString(xmlstr)
                xmlstr = startxml + xmlstr + endxml
                print("str---->", xmlstr)
                dtres['response'] = xmlstr

            else:
                res['status'] = 'false'
                dtres['token'] = ''
        else:
            res['status'] = 'false'
            dtres['token'] = ''
            dtres['response'] = "<error>Invalid Parameters</error>"

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        traceback.print_exc()


@csrf_exempt
def ret_module_details1(request):
    cursor = connection.cursor()
    try:
        dataObj = {}
        res = {}
        count = 0
        tdate = ''
        jsonData = request.POST.get('json')
        if jsonData == '' or not jsonData:
            jsonData = request.form['json']
        if jsonData != '' or jsonData:
            jsonObj = json.loads(jsonData)
            print("json obj--->", jsonObj)
            dataObj['UserId'] = jsonObj['LoginId']
            dataValue = json.dumps(jsonObj['modules'])
            dataList = json.loads(dataValue)
            data = dataList[0]
            currentdate = datetime.datetime.now()

            print("datalist---->", dataList)

            c = len(dataList)
            print("c---> ", c)

            i = 0
            for i in range(c):
                if dataList[i]['Eventname'] == '' or not dataList[i]['Eventname']:
                    dataList[i]['Eventname'] = '--'
                if dataList[i]['Action'] == '' or not dataList[i]['Action']:
                    dataList[i]['Action'] = '--'
                if dataList[i]['Meeting_ID'] == '' or not dataList[i]['Meeting_ID']:
                    dataList[i]['Meeting_ID'] = '--'
                if dataList[i]['Agenda_ID'] == '' or not dataList[i]['Agenda_ID']:
                    dataList[i]['Agenda_ID'] = '--'
                if dataList[i]['Level'] == '' or not dataList[i]['Level']:
                    dataList[i]['Level'] = '--'
                if dataList[i]['Value'] == '' or not dataList[i]['Value']:
                    dataList[i]['Value'] = '--'
                if dataList[i]['Document_ID'] == '' or not dataList[i]['Document_ID']:
                    dataList[i]['Document_ID'] = '--'
                if dataList[i]['deviceInfo'] == '' or not dataList[i]['deviceInfo']:
                    dataList[i]['deviceInfo'] = '--'
                if dataList[i]['Date'] == '' or not dataList[i]['Date']:
                    tdate = ''
                else:
                    tdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # query = "Insert Into activity_logs_modules (UserID,EventName,Date,Action,Mid,aid,Level,Value,Document_ID,deviceInfo,InsertDateTime)" \
                #         "values('" + dataObj['UserId'] + "','" + data['Eventname'] + "','" + data['Date'] + "','" + data[
                #             'Action'] + "','" + data['Meeting_ID'] + "'" \
                #                                                      ",'" + data['Agenda_ID'] + "','" + data[
                #             'Level'] + "','" + data['Value'] + "','" + data['Document_ID'] + "','" + data[
                #             'deviceInfo'] + "'," \
                #                             "'" + str(currentdate) + "')"
                query = "Insert Into activity_logs_modules (UserID,EventName,Date,Action,Mid,aid,Level,Value,Document_ID,deviceInfo,InsertDateTime)" \
                        "values('" + dataObj['UserId'] + "','" + dataList[i]['Eventname'] + "','" + dataList[i][
                            'Date'] + "','" + dataList[i][
                            'Action'] + "','" + dataList[i]['Meeting_ID'] + "'" \
                                                                            ",'" + dataList[i]['Agenda_ID'] + "','" + \
                        dataList[i][
                            'Level'] + "','" + dataList[i]['Value'] + "','" + dataList[i]['Document_ID'] + "','" + \
                        dataList[i][
                            'deviceInfo'] + "'," \
                                            "'" + tdate + "')"
                print(query)
            c1 = cursor.execute(query)
            print("c1--->", c1)
            if (c1 == 0):
                count += 1;
                if (count == c):
                    res['status'] = 'true'
            else:
                res['status'] = "Something Sent Wrong";

            return JsonResponse(res)
        else:
            res['status'] = 'Failure'
            res['message'] = "Parameters are empty."
            return JsonResponse(res)
    except:
        traceback.print_exc()


def RemoveFiles(userid, id):
    cursor = connection.cursor()
    try:
        query = "select userid,filename as doc from emeet_briefcase where id='" + id + "' and userid='" + userid + "' "
        cursor.execute(query)
        filesData = cursor.fetchall()
        print("filedata-----> ", filesData)

        fs = FileSystemStorage()

        if len(filesData) > 0:
            path = basepath + "static/Briefcase/" + filesData[0][0] + "/" + filesData[0][1]
            print('path--->', path)
            if (fs.exists(path)):
                fs.delete(path)

            res1 = cursor.execute("Delete from emeet_briefcase where id='" + id + "' and userid='" + userid + "'")
            print("res1----> ", res1)
            if res1 == 0:
                return True
            else:
                return False
        else:
            return False
    except:
        traceback.print_exc()
        return False


@csrf_exempt
def ret_removeBriefcase(request):
    cursor = connection.cursor()
    try:
        query = request.POST.get('userid')
        userid = ''
        token = ''
        id = ''
        if query == '' or not query:
            userid = object.decryptString(request.form['userid'])
            id = object.decryptString(request.form['id'])
            token = object.decryptString(request.form['token'])
        else:
            userid = object.decryptString(request.POST.get('userid'))
            id = object.decryptString(request.POST.get('id'))
            token = object.decryptString(request.POST.get('token'))

        res = {}
        dtres = {}
        print('======>>>>>', id, "||", token, "||", userid)

        if token or token != '':
            cursor.execute("select * from emeet_manageusers where userid='" + userid + "' and token='" + token + "' ")
            queryData = cursor.fetchall()
            print("query data---> ", queryData)

            if len(queryData) > 0:
                result = RemoveFiles(userid, id)
                dtres['response'] = str(result)
                dtres['token'] = token
                res['status'] = 'true'
            else:
                dtres['response'] = "Invalid token"
                dtres['token'] = ''
                res['status'] = 'false'

        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        # res['data'] = dtres
        print("response----------------------->", res)
        return JsonResponse(res)
    except:
        res = {}
        dtres = {}
        result = traceback.print_exc()
        dtres['response'] = "Error" + result
        dtres['token'] = ''
        res['status'] = 'true'
        res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
        return JsonResponse(res)


@csrf_exempt
def Mail(request):
    res = {}
    dtres = {}

    try:
        query = request.POST.get('userid')
        userid1 = ""
        search = ""
        token = ""
        timeStamp = ""
        fid = ""

        if query == "" or not query:
            token = object.decryptString(request.form['token'])
            userid1 = object.decryptString(request.form['userid'])
            search = object.decryptString(request.form['text'])
            timeStamp = object.decryptString(request.form['timeStamp'])
            fid = object.decryptString(request.form['fid'])
        else:
            token = object.decryptString(request.POST.get('token'))
            userid1 = object.decryptString(request.POST.get('userid'))
            search = object.decryptString(request.POST.get('text'))
            timeStamp = object.decryptString(request.POST.get('timeStamp'))
            fid = object.decryptString(request.POST.get('fid'))

        if token and token != "":
            cursor = connection.cursor()
            userid = token.split('_')
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1 + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            list1 = []
            if len(userlist) > 0:
                # select userid,ename,email from emeet_manageusers where (userid like '%p%' or ename like '%p%' or email like '%p%') and committee not in('usrmanage','admin') and (committee like '%,1,%' or committee like '1,%' or committee like '%,1'  or committee='1') order by email
                cursor.execute(
                    "select userid,ename,email from emeet_manageusers where (userid like '%" + search + "%' or ename like '%" + search + "%' or email like '%" + search + "%') and committee not in('usrmanage','admin') and (committee like '%," + fid + ",%' or committee like '" + fid + ",%' or committee like '%," + fid + "'  or committee='" + fid + "') order by email")
                userlist1 = cursor.fetchall()
                if len(userlist1) > 0:
                    for u in userlist1:
                        robj = {}
                        robj['userid'] = u[0]
                        robj['ename'] = u[1]

                        robj['email'] = u[2]

                        list1.append(robj)
                    dtres['token'] = userlist[0][0]
                    dtres['response'] = list1
                    res['status'] = 'true'
                else:
                    dtres['token'] = userlist[0][0]
                    dtres['response'] = list1
                    res['status'] = 'true'
            else:
                dtres['token'] = ''
                res['status'] = 'false'
        else:
            dtres['token'] = ""
            dtres['response'] = "invalid parameters"
            res['status'] = 'false'



    except Exception as e:
        traceback.print_exc()
        dtres['token'] = ""
        dtres['response'] = str(e)
        res['status'] = "false"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response------------------->", res)
    return JsonResponse(res)


@csrf_exempt
def ret_msg(request):
    res = {}
    dtres = {}

    userid = request.POST.get('userid')
    token = request.POST.get('token')

    if userid == "" or not userid:
        userid = object.decryptString(request.form['userid'])
        token = object.decryptString(request.form['token'])
    else:
        userid = object.decryptString(request.POST.get('userid'))
        token = object.decryptString(request.POST.get('token'))

    try:
        cursor = connection.cursor()
        cursor.execute("select committee from emeet_manageusers where userid='" + userid + "'")
        userlist = cursor.fetchall()

        comp = userlist[0][0].split(',')
        ml = []
        if len(userlist) > 0:
            qu = "select * from emeet_msg where comm = '0'"
            for c in comp:
                qu += " or comm like '%" + str(c) + "%'";
            qu += " order by dt desc LIMIT  100"
            cursor.execute(qu)
            ulist = cursor.fetchall()
            for u in ulist:
                myobj = {}
                myobj['id'] = u[0]
                myobj['msg'] = u[1]
                myobj['status'] = u[4]
                myobj['dt'] = u[2].strftime("%d/%m/%Y %I:%M:%S %p")
                myobj['comm'] = u[3]
                ml.append(myobj)
            dtres['token'] = token
            dtres['response'] = json.dumps(ml)
            res['status'] = "true"
        else:
            dtres['token'] = token
            dtres['response'] = "No records found"
            res['status'] = "false"

    except:
        traceback.print_exc()
        dtres['token'] = ""
        dtres['response'] = "No records found"
        res['status'] = "false"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response------------------------>", res)
    return JsonResponse(res)


@csrf_exempt
def ret_audittrail(request):
    cursor = connection.cursor()
    jsonData = request.POST.get('json')
    ag_id = ""
    mid = ""
    fid = ""
    userid = ""
    level = ""
    token = ""

    res = {}
    dtres = {}

    try:
        if jsonData == "" or not jsonData:
            jsonData = object.decryptString(request.Form['json'])
        else:
            jsonData = object.decryptString(request.POST.get('json'))

        js = json.loads(jsonData)
        print("audit js---->", js)
        userid = js['userid']
        token = js['token']
        mid = js['mid']
        fid = js['fid']
        level = js['level']
        ag_id = js['ag_id']

        currentDate = datetime.datetime.now()

        if token != "" or token:
            user = token.split('_')
            cursor.execute(
                "select token from emeet_manageusers where userid='" + user[0] + "' and token='" + token + "' ")
            tokenValue = cursor.fetchall()

            if len(tokenValue) > 0:
                query = "insert into emeet_audit(fid,mid,ag_id,level,userid,dt) values('" + fid + "','" + mid + "','" + ag_id + "'," \
                                                                                                                                "'" + level + "','" + userid + "','" + str(
                    currentDate) + "')"
                print("query---->", query)
                result = cursor.execute(query)
                print("result--->", result)

                if result == 1:
                    res['status'] = "true"
                    dtres['token'] = tokenValue[0][0]
                    dtres['response'] = "true"
                else:
                    res['status'] = 'false'
                    dtres['token'] = tokenValue[0][0]
                    dtres['response'] = 'false'
            else:
                res['status'] = 'false'
                dtres['token'] = ""
                dtres['response'] = 'false'

        else:
            res['status'] = 'false'
            dtres['token'] = ""
            dtres['response'] = 'Invalid parameters'
    except:
        traceback.print_exc()
        res['status'] = 'false'
        dtres['token'] = ""
        dtres['response'] = 'Error'

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response------------------------>", res)
    return JsonResponse(res)


@csrf_exempt
def ret_snapshot(request):
    res = {}
    dtres = {}
    try:
        userid = request.POST.get('userid')
        fid = ""
        mid = ""
        token = ""
        agid = ""
        level = ""
        pgno = ""

        if userid == "" or not userid:
            userid = object.decryptString(request.form['userid'])
            fid = object.decryptString(request.form['fid'])
            mid = object.decryptString(request.form['mid'])
            token = object.decryptString(request.form['token'])
            agid = object.decryptString(request.form['ag_id'])
            level = object.decryptString(request.form['level'])
            pgno = object.decryptString(request.form['pgno'])
        else:
            userid = object.decryptString(request.POST.get('userid'))
            fid = object.decryptString(request.POST.get('fid'))
            mid = object.decryptString(request.POST.get('mid'))
            token = object.decryptString(request.POST.get('token'))
            agid = object.decryptString(request.POST.get('ag_id'))
            level = object.decryptString(request.POST.get('level'))
            pgno = object.decryptString(request.POST.get('pgno'))

        if userid and userid != "" and fid and fid != "" and mid and mid != "" and token and token != "" and agid and agid != "" and level and level != "" and pgno and pgno != "":
            userid1 = token.split("_")
            cursor = connection.cursor()
            cursor.execute(
                "select token from emeet_manageusers where userid='" + userid1[0] + "' and token='" + token + "'")
            userlist = cursor.fetchall()
            if len(userlist) > 0:
                a = cursor.execute(
                    "insert into emeet_usr_snap(fid,mid,ag_id,level,pageno,userid,dt) values('" + fid + "','" + mid + "','" + agid + "','" + level + "','" + pgno + "','" + userid + "',now())")
                if a == 1:
                    dtres['token'] = userlist[0][0]
                    dtres['response'] = "true"
                    res['status'] = "true"
                else:
                    dtres['token'] = ""
                    dtres['response'] = "false"
                    res['status'] = "false"
            else:
                dtres['token'] = ""
                dtres['response'] = "false"
                res['status'] = "false"
        else:
            dtres['token'] = ""
            dtres['response'] = "Invalid parameters"
            res['status'] = "false"

    except Exception as e:
        traceback.print_exc()
        dtres['response'] = str(e)
        res['status'] = "false"

    res['data'] = object.encryptString(json.dumps(dtres, separators=(',', ':')))
    print("response------------------------>", res)
    return JsonResponse(res)


#########################################################################################################
########################## chat methods #################

def index(request):
    return render(request, 'chat/index.html')


@csrf_exempt
def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})


########################################   presentor module  ###################################

def startgroup(request):
    print("strt grp request--->", request)
    msg1 = request.POST.get('message')
    msg = json.loads(msg1)
    print("msg-->", msg)
    mid = msg['mid']
    userid = msg['userid']
    url = 'wss://' + base11 + '/ws/chat/EmeetingTest/'
    print("start grp ip-----> ", mid, userid)
    groupDict = {}
    groupDict['mid'] = mid
    groupDict['userid'] = userid
    groupDict['url'] = url

    print('groupdict--->', groupDict)
    res = {}
    res['data'] = object.encryptString(json.dumps(groupDict, separators=(',', ':')))
    print("response------------------------>", res)
    return JsonResponse(res)


def startPresentation(request):
    res = {}
    res['data'] = 'start  presenation'
    print("response------------------------>", res)
    return JsonResponse(res)



