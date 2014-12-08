__author__ = 'danielkershaw'
import datetime

def serilize(submission):
    tmp = {}

    for v in vars(submission):
        if v == 'subreddit':
            tmp[v] = "{0}".format(vars(submission)[v]).encode("utf8")
        elif v == 'created_utc':
            tmp[v] = datetime.datetime.fromtimestamp(int(vars(submission)[v])).strftime('%Y-%m-%d %H:%M:%S')
        elif v == 'author':
            tmp[v] = "{0}".format(vars(submission)[v]).encode("utf8")
        elif v == 'replies':
            #TODO replites to list of ids
            tmp[v] = "replies"
        elif v == "is_root":
            tmp[v] = vars(submission)[v].encode("utf8")
        elif v == "submission":
            tmp[v] = "{0}".format(vars(submission)[v]).encode("utf8")
        elif v != 'reddit_session' and v != 'comment' and v != '_replies' and v != '_submission' and v != '_comments' and v != '_comments_by_id':
            tmp[v] = vars(submission)[v].encode("utf8")
    return tmp

def serlizeComment(comment):
    tmp = {}
    tmp["approved_by"]= "{0}".format(comment.approved_by).encode("utf8")
    tmp["author"] = "{0}".format(comment.author).encode("utf8")
    tmp["author_flair_css_class"] = "{0}".format(comment.author_flair_css_class).encode("utf8")
    tmp["author_flair_text"] = "{0}".format(comment.author_flair_text).encode("utf8")
    tmp["banned_by"]=comment.banned_by.encode("utf8")
    tmp["body"]=comment.body.encode("utf8")
    tmp["body_html"]=comment.body_html.encode("utf8")
    tmp["controversiality"]=comment.controversiality.encode("utf8")
    tmp["created"]=comment.created.encode("utf8")
    tmp["created_utc"]=datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
    tmp["distinguished"]=comment.distinguished.encode("utf8")
    tmp["downs"]=comment.downs.encode("utf8")
    tmp["edited"]=comment.edited.encode("utf8")
    tmp["fullname"]=comment.fullname.encode("utf8")
    tmp["gilded"]=comment.gilded.encode("utf8")
    tmp["has_fetched"]=comment.has_fetched.encode("utf8")
    tmp["id"]=comment.id.encode("utf8")
    tmp["is_root"]=comment.is_root.encode("utf8")
    tmp["json_dict"]=comment.json_dict.encode("utf8")
    tmp["likes"]=comment.likes.encode("utf8")
    tmp["link_id"]=comment.link_id.encode("utf8")
    tmp["mod_reports"]=comment.mod_reports.encode("utf8")
    tmp["name"]=comment.name.encode("utf8")
    tmp["num_reports"]=comment.num_reports.encode("utf8")
    tmp["parent_id"]=comment.parent_id.encode("utf8")
    tmp["permalink"]=comment.permalink.encode("utf8")
    tmp["replies"]=comment.replies.encode("utf8")
    tmp["report_reasons"]=comment.report_reasons.encode("utf8")
    tmp["saved"]=comment.saved.encode("utf8")
    tmp["score"]=comment.score.encode("utf8")
    tmp["score_hidden"]=comment.score_hidden.encode("utf8")
    tmp["submission"]= "{0}".format(comment.submission).encode("utf8")
    tmp["subreddit"]= "{0}".format(comment.subreddit).encode("utf8")
    tmp["subreddit_id"]= "{0}".format(comment.subreddit_id).encode("utf8")
    tmp["ups"]=comment.ups.encode("utf8")
    if hasattr(comment, "parent_id"):
        tmp["parent_id"] = comment.parent_id.encode("utf8")
    if hasattr(comment, "_replies"):
        t = []
        for tt in comment._replies:
            t.append(tt.fullname.encode("utf8"))
        tmp["replies"] = t
    tmp["ups"]=comment.ups.encode("utf8")
    tmp["user_reports"]=comment.user_reports.encode("utf8")
    return tmp