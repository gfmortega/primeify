import PySimpleGUI as sg
from PIL import Image
from tkinter import TclError

from enum import Enum, auto

from scuffed_clustering import cluster
from grid_painter import paint_grid, paint_text_grid
from prime_finder import primeify

class State(Enum):
    NO_ORIG_IMAGE = auto()
    UNCLEANED_ORIG_IMAGE = auto()
    CLEANED_ORIG_IMAGE = auto()
    PRIME_DONE = auto()

def main():
    orig_image_filename = None
    current_image, h, w = None, None, None
    clean_image, new_h, new_w = None, None, None
    clustered_pixels = None
    window, values = None, None
    prime, color = None, None

    def get_orig_filename():
        return values['_SELECT_ORIG_IMAGE_'].split('/')[-1].split('.')[0]

    def enter(state):
        if state == State.NO_ORIG_IMAGE:
            window['_SHRINK_CLEAN_'].update(visible=False)
            window['_REFRESH_'].update(visible=False)
            window['_PRIME_'].update(visible=False)

            window['_CLEANING_STATUS_'].update('')
            window['_DIMENSIONS_TEXT_'].update('')
            window['_NEW_H_'].update('')
            window['_NEW_W_'].update('')
            window['_OUTPUT_'].update('')
            window['_K_'].update('')
            
            window['_CLEAN_IMAGE_'].update(filename='')
            window['_ORIG_IMAGE_'].update(filename='')

        elif state == State.UNCLEANED_ORIG_IMAGE:
            window['_SHRINK_CLEAN_'].update(visible=True)
            window['_REFRESH_'].update(visible=False)
            window['_PRIME_'].update(visible=False)
            
            window['_CLEANING_STATUS_'].update('')
            window['_DIMENSIONS_TEXT_'].update(f'Dimensions: {h} x {w}')
            window['_NEW_H_'].update(str(h))
            window['_NEW_W_'].update(str(w))
            window['_OUTPUT_'].update(get_orig_filename())
            window['_K_'].update('')

            window['_CLEAN_IMAGE_'].update(filename='')
            window['_ORIG_IMAGE_'].update(filename=orig_image_filename)

        elif state == State.CLEANED_ORIG_IMAGE:
            window['_REFRESH_'].update(visible=True)
            window['_PRIME_'].update(visible=True)

            window['_CLEANING_STATUS_'].update("Done!  Clean the image (if you want), then press Refresh")
            
            window['_CLEAN_IMAGE_'].update(filename=f'./{values["_OUTPUT_"].strip()}/{values["_OUTPUT_"].strip()}.png')

        elif state == State.PRIME_DONE:
            window['_PRIME_DONE_'].update('Done prime-ifying!')
            window['_BG_RGB_'].update('255,255,255', visible=True)
            window['_BG_LABEL_'].update(visible=True)

            window['_PRIME_PAINTING_'].update(visible=True)
            
    def exeunt(state):
        if state == State.NO_ORIG_IMAGE:
            pass

        elif state == State.UNCLEANED_ORIG_IMAGE:
            pass

        elif state == State.CLEANED_ORIG_IMAGE:
            pass

        elif state == State.PRIME_DONE:
            window['_PRIME_DONE_'].update('')
            window['_BG_RGB_'].update(visible=False)
            window['_BG_LABEL_'].update(visible=False)
            window['_PRIME_PAINTING_'].update(visible=False)

    state = State.NO_ORIG_IMAGE
    def transition(state, new_state):
        exeunt(state)
        enter(new_state)
        return new_state

    column0 = [
        [
            sg.Text('Select PNG:'),
            sg.Input('', enable_events=True, key='_SELECT_ORIG_IMAGE_'),
            sg.FileBrowse(target='_SELECT_ORIG_IMAGE_')
        ],
        [sg.Text('', key='_DIMENSIONS_TEXT_')],
        [sg.Image(key='_ORIG_IMAGE_')]
    ]
    column1 = [
        [sg.Text('Number of colors in pixel art:'), sg.Combo([str(k) for k in range(2,10+1)], size=(5, 1), key='_K_')],
        [sg.Text('For reasonably fast prime-ifying, we recommend ~1-3k pixels in cleaned image')],
        [sg.Text('New width'), sg.In(size=(5, 1), key='_NEW_W_')],
        [sg.Text('New height'), sg.In(size=(5, 1), key='_NEW_H_')],
        [
            sg.Column([[sg.Button('Shrink + Clean', key='_SHRINK_CLEAN_', visible=False)]]),
            sg.Column([[sg.Button('Refresh', visible=False, key='_REFRESH_')]]),
        ],
        [sg.Text('', key='_CLEANING_STATUS_')],
        [sg.Image(key='_CLEAN_IMAGE_')]
    ]
    column2 = [
        [sg.Text('Output Name:'), sg.In(size=(10, 1), key='_OUTPUT_')],
        [sg.Column([[sg.Button('Prime-ify!', visible=False, key='_PRIME_')]])],
        [
            sg.Column([[sg.Text('Output BG Color (RGB):', visible=False, key='_BG_LABEL_')]]),
            sg.Column([[sg.In(size=(25, 1), visible=False, key='_BG_RGB_')]])
        ],
        [sg.Text('', key='_PRIME_DONE_')],
        [sg.Button('Output to Painting!', visible=False, key='_PRIME_PAINTING_')]
    ]

    layout = [[sg.Column(column0), sg.VSeparator(), sg.Column(column1), sg.VSeparator(), sg.Column(column2)]]
    window = sg.Window(
        title='Prime-ify!',
        layout=layout,
    )

    
    # event loop
    while True:
        event, values = window.read()
        # print(event, values)
        if event == '_SELECT_ORIG_IMAGE_':
            orig_image_filename = values['_SELECT_ORIG_IMAGE_']
            try:
                current_image = Image.open(orig_image_filename).convert('RGB')
                h = current_image.height
                w = current_image.width
                state = transition(state, State.UNCLEANED_ORIG_IMAGE)

            except TclError:
                sg.popup_error('PySimpleGUI can only process .png file format')
            except Exception as E:
                sg.popup_error(str(E))

        elif event == '_SHRINK_CLEAN_':
            if current_image:
                if values['_OUTPUT_'].strip():
                    try:
                        new_h = int(values['_NEW_H_'])
                        new_w = int(values['_NEW_W_'])
                        assert(1 <= new_h <= h)
                        assert(1 <= new_w <= w)
                    except Exception as E:
                        sg.popup_error("Please ensure that the new dimensions are positive integers leq the original dimensions")
                        continue

                    try:
                        k = int(values['_K_'])
                    except Exception as E:
                        sg.popup_error("Please decide on k, the number of colors in the pixel art")
                        continue

                    if k > new_h*new_w:
                        sg.popup_error("Please pick a k that's geq the number of pixels in the new dimensions")
                        continue

                    pixel_h = h//new_h
                    pixel_w = w//new_w
                    pixels = list(current_image.getdata())
                    compressed_pixels = [pixels[i*w*pixel_h + j*pixel_w] for i in range(new_h) for j in range(new_w)]
                    clustered_pixels = cluster(k, compressed_pixels)
                    paint_grid(grid=clustered_pixels, w=new_w, h=new_h, filename=values['_OUTPUT_'].strip())

                    state = transition(state, State.CLEANED_ORIG_IMAGE)
                else:
                    sg.popup_error("Please decide on an output file name!")
            else:
                sg.popup_error("No image selected yet")
        
        elif event == '_REFRESH_':
            if values['_OUTPUT_'].strip():
                try:
                    window['_CLEAN_IMAGE_'].update(filename=f'./{values["_OUTPUT_"].strip()}/{values["_OUTPUT_"].strip()}.png')
                except Exception as E:
                    sg.popup_error("The file could not be found")
            else:
                sg.popup_error("Please decide on an output file name!")

        elif event == '_PRIME_':
            if values['_OUTPUT_'].strip():
                prime, colors = primeify(clustered_pixels, w=new_w, h=new_h)
                name = values['_OUTPUT_'].strip()
                print(colors)
                with open(f'{name}/{name}-prime-number.txt', 'w') as writer:
                    print(''.join(prime), file=writer)

                with open(f'{name}/{name}-prime-grid.txt', 'w') as writer:
                    for i in range(new_h):
                        print(''.join(prime[i*new_w:(i+1)*new_w]))
                        print(''.join(prime[i*new_w:(i+1)*new_w]), file=writer)

                state = transition(state, State.PRIME_DONE)
            else:
                sg.popup_error("Please decide on an output name for the prime!")

        elif event == '_PRIME_PAINTING_':
            if values['_OUTPUT_'].strip():
                try:
                    bg = tuple(map(int, values['_BG_RGB_'].split(',')))
                except Exception as E:
                    sg.popup_error("Please input a valid RGB triple for the Output BG color")
                    continue

                invert = {value: key for key, value in colors.items()}
                paint_text_grid(grid=prime, w=new_w, h=new_h, colors=invert, bg=bg, filename=values['_OUTPUT_'].strip())
                state = transition(state, State.PRIME_DONE)
            else:
                sg.popup_error("Please decide on an output name for the prime!")

        elif event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == '__main__':
    main()
