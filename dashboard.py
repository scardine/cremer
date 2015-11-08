# encoding: utf-8
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.utils import get_admin_site_name
from jet.dashboard.dashboard_modules import google_analytics


class StatisticsModule(modules.DashboardModule):
    title = _('Statistics')
    template = 'helpdesk/statistics.html'


class GetItineraryModule(modules.DashboardModule):
    title = _('Get Itinerary')
    template = 'helpdesk/itinerary.html'


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(modules.Feed)

        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
        self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)

        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ],
            column=0,
            order=0
        ))

        self.children.append(StatisticsModule())
        self.children.append(GetItineraryModule())

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=1,
            order=0
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('auth.*',),
            column=2,
            order=0
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=0,
            order=1
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Sabre News'),
            feed_url='http://apps.shareholder.com/rss/rss.aspx?channels=10466&companyid=AMDA-2OXSEI&sh_auth=982801804%2E0%2E0%2E42317%2E046b3599c53e98ac941498424013e00c',
            limit=5,
            column=1,
            order=1
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Other Applications'),
            children=[
                {
                    'title': _('Argo IT TMS'),
                    'url': 'http://www2.argoit.com.br/solucoes/tms',
                    'external': True,
                },
                {
                    'title': _('Sabre Developer Studio'),
                    'url': 'https://developer.sabre.com/',
                    'external': True,
                },
                {
                    'title': _('VoyEnBus'),
                    'url': 'http://www.voyenbus.com/',
                    'external': True,
                },
            ],
            column=2,
            order=1
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)

        self.children.append(modules.ModelList(
            title=_('Application models'),
            models=self.models(),
            column=0,
            order=0
        ))
        self.children.append(modules.RecentActions(
            include_list=self.get_app_content_types(),
            column=1,
            order=0
        ))