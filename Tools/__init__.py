__author__ = 'danielkershaw'
import datetime

def serilize(submission):
    tmp = {}

    for v in vars(submission):
        if v == 'subreddit':
            tmp[v] = "{0}".format(vars(submission)[v])
        elif v == 'created_utc':
            tmp[v] = datetime.datetime.fromtimestamp(int(vars(submission)[v])).strftime('%Y-%m-%d %H:%M:%S')
        elif v == 'author':
            tmp[v] = "{0}".format(vars(submission)[v])
        elif v == 'replies':
            #TODO replites to list of ids
            tmp[v] = "replies"
        elif v == "is_root":
            tmp[v] = vars(submission)[v]
        elif v == "submission":
            tmp[v] = "{0}".format(vars(submission)[v])
        elif v != 'reddit_session' and v != 'comment' and v != '_replies' and v != '_submission' and v != '_comments' and v != '_comments_by_id':
            tmp[v] = vars(submission)[v]
    return tmp

def serlizeComment(comment):
    tmp = {}
    tmp["approved_by"]= "{0}".format(comment.approved_by)
    tmp["author"] = "{0}".format(comment.author)
    tmp["author_flair_css_class"] = "{0}".format(comment.author_flair_css_class)
    tmp["author_flair_text"] = "{0}".format(comment.author_flair_text.encode('utf-8').strip())
    tmp["banned_by"]=comment.banned_by
    tmp["body"]=comment.body
    tmp["body_html"]=comment.body_html
    tmp["controversiality"]=comment.controversiality
    tmp["created"]=comment.created
    tmp["created_utc"]=datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
    tmp["distinguished"]=comment.distinguished
    tmp["downs"]=comment.downs
    tmp["edited"]=comment.edited
    tmp["fullname"]=comment.fullname
    tmp["gilded"]=comment.gilded
    tmp["has_fetched"]=comment.has_fetched
    tmp["id"]=comment.id
    tmp["is_root"]=comment.is_root
    tmp["json_dict"]=comment.json_dict
    tmp["likes"]=comment.likes
    tmp["link_id"]=comment.link_id
    tmp["mod_reports"]=comment.mod_reports
    tmp["name"]=comment.name
    tmp["num_reports"]=comment.num_reports
    tmp["parent_id"]=comment.parent_id
    tmp["permalink"]=comment.permalink
    tmp["replies"]=comment.replies
    tmp["report_reasons"]=comment.report_reasons
    tmp["saved"]=comment.saved
    tmp["score"]=comment.score
    tmp["score_hidden"]=comment.score_hidden
    tmp["submission"]= "{0}".format(comment.submission)
    tmp["subreddit"]= "{0}".format(comment.subreddit)
    tmp["subreddit_id"]= "{0}".format(comment.subreddit_id)
    tmp["ups"]=comment.ups
    if hasattr(comment, "parent_id"):
        tmp["parent_id"] = comment.parent_id
    if hasattr(comment, "_replies"):
        t = []
        for tt in comment._replies:
            t.append(tt.fullname)
        tmp["replies"] = t
    tmp["ups"]=comment.ups
    tmp["user_reports"]=comment.user_reports
    return tmp