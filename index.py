import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os
import importlib
from app import app,server
from presentation import slide_order, prev_text, next_text



for x in os.listdir(os.getcwd()+'/slides'):
    slide_name = x.split('.')[0]
    if slide_name in slide_order:
        globals()['slide_'+slide_name] = importlib.import_module('slides.'+slide_name)



def slide_dict():
    d = {v:k for k,v in dict(enumerate(slide_order)).items()}
    d['/'] = 0
    return d



nav_style = dict(
    textAlign='center',
)



def nav_button_div(text):
    '''helper function to return the navigation buttons easily'''
    return html.Div(  children=[
        dbc.Button(
            html.H4(text),
            style=dict(
                width='100%'
            ),
            color='primary',
            outline=True,

        )
    ], className = "shadow-lg rounded mb-2" )

app.layout = html.Div(style = {'background-image': 'url("/assets/6.jpg"' ,
#  '-webkit-background-size': 'cover',
 # '-moz-background-size': 'cover',
 # '-o-background-size': 'cover',
 # 'background-size': 'cover'    },
},
children= [ dbc.Container(children= html.Div([

    dcc.Location(id='url', refresh=False),
    dbc.Container(fluid=True,children=[
        html.Div(id='current-slide',style=dict(display='none',children='')),
        # nav div
        dbc.Row(style=dict(height='auto',position='sticky',margin='10 px'),
        children=[

                  dbc.Col(width=4,style=nav_style,children=[
                  dcc.Link(
                    id='previous-link',
                    href='',
                    children=nav_button_div('<< Previous'),
                ),
            ]),

            # slide count
            dbc.Col(style=dict(width=4, textAlign='center' ), children=[
                dbc.DropdownMenu(
                    id='slide-count',
                    bs_size='lg',

                    children = [
                    dbc.DropdownMenuItem(
                        s,
                        href='/'+s,
                    )
                    for s in slide_order
                ] )
            ]), # end slide count

            # next
            dbc.Col(width=4,style=nav_style,children=[
                dcc.Link(
                    id='next-link',
                    href='',
                    children=nav_button_div('Next >>'),
                ),
            ]), # end next
        ]),
    ], style={'position': 'relative', 'zIndex': '10000' }),

    # slide content
    html.Div(id='page-content'),
    html.Div( html.Footer(html.Hr([], className = "divider  bg-primary")), style = {'margin-top' : '35rem'})
]),  )])


# url function
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')],
)
def change_slide(pathname):
    '''gets current slide goes either back a slide or forward a slide'''
    if pathname=='/' or pathname=='/'+slide_order[0] or pathname==None:
        return globals()['slide_'+slide_order[0]].content
    else:
        try:
            pathname = pathname.split('/')[1].strip()
            return globals()['slide_'+pathname].content
        except:
            return '404'

# navigation functions
@app.callback(
    [Output('next-link','href'),
     Output('previous-link','href')],
    [Input('current-slide','children')],
    [State('url','pathname')]
)
def navigate(current_slide,pathname):
    '''
    - listens to
        - next/previous buttons
    - determines the current slide name
    - changes 'next' and 'previous' to the names of the slides on each side\
     of the current slide
    - if this is the last or first slide, 'next' or 'previous' will just\
     refresh the current slide
    '''
    next_slide = current_slide
    previous_slide = current_slide
    current_order = slide_dict()[current_slide]
    num_slides = max(slide_dict().values())

    # if we're on the first slide, clicking 'previous' just refreshes the page
    if current_order != 0:
        previous_slide = slide_order[current_order-1]
    # if we're on the last slide, clicking 'next' just refreshes the page
    if current_order != num_slides:
        next_slide = slide_order[current_order+1]

    return next_slide, previous_slide

@app.callback(
    Output('current-slide','children'),
    [Input('url','pathname')]
)
def set_slide_state(pathname):
    '''
    returns the name of the current slide based on the pathname
    this runs first and triggers navigate (changes the relative hrefs of\
     'next' and 'previous')
    '''
    if pathname==None:
        return '/'
    if '/' in pathname:
        if pathname=='/':
            return pathname
        return pathname.split('/')[1].strip()

@app.callback(
    Output('slide-count','label'),
    [Input('current-slide','children')]
)
def update_slide_count(current_slide):
    '''shows the current slide number out of the total'''
    total = len(slide_order)
    current = slide_dict()[current_slide] + 1
    return '{}/{}'.format(current,total)

if __name__=='__main__':
      app.run_server(port=8050,host = 'localhost',   debug=True, dev_tools_ui
      = True,dev_tools_props_check= True )
