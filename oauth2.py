from dropbox.client import DropboxOAuth2Flow, DropboxClient

credentials = {
        'api-key' : 'm6kf74jc20wbvyj',
        'app-secret' : 'c5l9kswk565a62z'
        }



def get_dropbox_auth_flow(web_app_session):
    redirect_uri =  "http://localhost"
    return DropboxOAuth2Flow(credentials['api-key'], 
            credentials['app-secret'],
            redirect_uri,
            web_app_session,
            'dropbox-auth-csrf-token')

#URL handler for /dropbox-auth-start
def dropbox_auth_start(web_app_session, request):
    authorize_url = get_dropbox_auth_flow(web_app_session).start()
    redirect_to(authorize_url)

#URL handler for /dropbox-auth-finish
def dropbox_auth_finish(web_app_session, request):
    try:
        access_token, user_id, url_state = get_dropbox_auth_flow(web_app_session).finish(request.query_params)
    except DropboxOAuth2Flow.BadRequestException, e:
        http_status(400)
    except DropboxOAuth2Flow.BadStateException, e:
        # Start the auth flow again.
        redirect_to("/dropbox-auth-start")
    except DropboxOAuth2Flow.CsrfException, e:
        http_status(403)
    except DropboxOAuth2Flow.NotApprovedException, e:
        flash('Not approved?  Why not?')
        return redirect_to("/home")
    except DropboxOAuth2Flow.ProviderException, e:
        logger.log("Auth error: %s" % (e,))
        http_status(403)

