import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np

def show_video_subtitle(frames, subtitle):
    fig, ax = plt.subplots()
    fig.show()

    text = plt.text(0.5, 0.1, "", 
        ha='center', va='center', transform=ax.transAxes, 
        fontdict={'fontsize': 15, 'color':'white', 'fontweight': 500})
    text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),
        path_effects.Normal()])

    #subs = subtitle.split()
    subs = subtitle
    inc = max(len(frames)/(len(subs)+1), 0.01)

    i = 0
    img = None
    for frame in frames:
        sub = " ".join(subs[:int(i/inc)])

        text.set_text(sub)

        if img is None:
            img = plt.imshow(frame)
        else:
            img.set_data(frame)
        fig.canvas.draw()
        i += 1


if __name__ == '__main__':
    video = np.load('video_face.npy')
    result = np.load('result_split.npy')
    show_video_subtitle(video, result)
