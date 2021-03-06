from routes.route import Route

chooser_routes = [
    Route("choose_index", "/",
          controller="cc.engine.chooser.views:chooser_view"),
    Route("choose_index", "/classic_chooser/",
          controller="cc.engine.chooser.views:classic_chooser_view"),
    Route("choose_results_one", "/results-one",
          controller="cc.engine.chooser.views:choose_results_view"),
    Route("choose_results_one", "/xhr_api",
          controller="cc.engine.chooser.views:xhr_api"),
    Route("choose_results_one", "/xmp",
          controller="cc.engine.chooser.views:choose_xmp_view"),
    Route("choose_get_html", "/get-html",
          controller="cc.engine.chooser.views:get_html"),
    Route("choose_get_rdf", "/get-rdf",
          controller="cc.engine.chooser.views:get_rdf"),
    Route("choose_non_web_popup", "/non-web-popup",
          controller="cc.engine.chooser.views:non_web_popup"),
    Route("choose_xmp_popup", "/metadata.xmp",
          controller="cc.engine.chooser.views:choose_xmp_view"),
    Route("choose_work_html_popup", "/work-html-popup",
          controller="cc.engine.chooser.views:work_email_popup"),
    Route("choose_work_html_send", "/work-email",
          controller="cc.engine.chooser.views:work_email_send"),

    Route("choose_wiki", "/wiki",
          controller="cc.engine.chooser.views:choose_wiki_redirect"),
    Route("choose_music", "/music",
          controller="cc.engine.chooser.views:outdated_choosers_redirect"),
    Route("choose_sampling", "/sampling",
          controller="cc.engine.chooser.views:outdated_choosers_redirect"),

    # "Special" choosers
    ## FSF choosers...
    ## (Actually, we no longer handle these ourselves, so they redirect
    ##  to gnu.org.)
    Route("choose_gpl", "/cc-gpl",
          controller="cc.engine.chooser.views:gpl_redirect"),
    Route("choose_lgpl", "/cc-lgpl",
          controller="cc.engine.chooser.views:gpl_redirect"),

    ## Public domain chooser
    Route("choose_publicdomain_landing", "/publicdomain-2",
          controller="cc.engine.chooser.views:publicdomain_landing"),
    Route("choose_publicdomain_confirm", "/publicdomain-3",
          controller="cc.engine.chooser.views:publicdomain_confirm"),
    Route("choose_publicdomain_result", "/publicdomain-4",
          controller="cc.engine.chooser.views:publicdomain_result"),
    
    ### General publicdomain partner page now redirects to CC0 partner
    Route("choose_publicdomain_partner", "/publicdomain-direct",
          controller="cc.engine.chooser.views:publicdomain_direct_redirect"),

    ## CC0 chooser
    Route("choose_cc0_landing", "/zero/",
          controller="cc.engine.chooser.views:cc0_landing"),
    Route("choose_cc0_waiver", "/zero/waiver",
          controller="cc.engine.chooser.views:cc0_waiver"),
    Route("choose_cc0_confirm", "/zero/confirm",
          controller="cc.engine.chooser.views:cc0_confirm"),
    Route("choose_cc0_results", "/zero/results",
          controller="cc.engine.chooser.views:cc0_results"),
    Route("choose_cc0_partner", "/zero/partner",
          controller="cc.engine.chooser.views:cc0_partner"),

    ## Public Domain Mark chooser
    Route("choose_pdmark_landing", "/mark/",
          controller="cc.engine.chooser.views:pdmark_landing"),
    Route("choose_pdmark_details", "/mark/details",
          controller="cc.engine.chooser.views:pdmark_details"),
    Route("choose_pdmark_results", "/mark/results",
          controller="cc.engine.chooser.views:pdmark_results"),
    Route("choose_pdmark_partner", "/mark/partner",
          controller="cc.engine.chooser.views:pdmark_partner"),
    ]

