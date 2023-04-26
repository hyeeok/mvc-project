import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# 각각의 컴포넌트에서 사용할 콜백 함수들을 모듈로부터 import합니다.
# from callbacks import register_callbacks
# 각각의 페이지 컴포넌트를 모듈로부터 import합니다.
from src.pages import login, search, company_info, all_company_info

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

navbar = dbc.NavbarSimple(
    brand="Greta MVC",
    brand_href="/",
    children=[
        # dbc.NavItem(dbc.NavLink("기업 검색", href="/search")),
        # dbc.NavItem(dbc.NavLink("전체 기업 정보 분석", href="/all_company_info")),
    ],
    sticky="top",
    id="navbar",
)

content = html.Div(id="page-content", style={"padding": "1rem 1.5rem"})

# 각 페이지 컴포넌트를 등록합니다.
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        content,
    ]
)


# Page Content
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
    #     return login.layout
    # elif pathname == "/search":
    #     return search.layout
    # elif pathname == "/company_info":
    #     return company_info.layout
    # elif pathname == "/all_company_info":
        return all_company_info.layout
    else:
        return "404 Error: Page not found"


# 컴포넌트들의 콜백 함수들을 등록합니다.
# register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
