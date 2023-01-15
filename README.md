# microstructure-plotter

**For those of you in the trenches, I offer ye this tool ⚔️.** 

This is a plotting tool designed to help visualize financial market data 📈 and trading system behavior 🤖 on the smallest timescales 🔎. 

As all things in life, when it comes to microstructure & HFT: _the devil is in the details_. 

Built using [Chaco](https://docs.enthought.com/chaco/index.html) 🌮.

![zoooooom](/assets/plotter_video.gif)

## Contents

- [⚠️Disclaimer](#⚠️disclaimer)
- [🧪Test It Out Right Now](#🧪test-it-right-out-now)
- [✨Features](#✨features)
- [🧠Illustrated Example](#🧠illustrated-example)
- [🗺️Plots Legend](#🗺️plots-legend)
- [💸Free Advice](#💸free-advice)
- [✏️Data Schema](#✏️data-schema)
- [🤔What is "Market Microstructure"?](#🤔what-is-market-microstructure)
- [🛞Installation](#🛞installation)
- [	📜Reqs](#📜reqs)
- [𓊍To Do](#𓊍to-do)
- [Citation](#citation)
- [License](#license)

## ⚠️Disclaimer

There is no α here. This is just a fancy wrapper on top of an open-source plotting package. 

You should _Bring Your Own Alpha_ (**B.Y.O.A.**). 

**HOWEVER**...for the trained eye, this simple type of visualization can be immensely helpful.

## 🧪Test It Right Out Now

After installing the package either via [pip](#🛞installation) or via [setup.py](#📜reqs), run this quick line to see this in action right now:

``` bash examples/example_1/plot_example.sh ``` 

or 

``` python examples/example_1/plot_example.py ``` 

**Right-click** 🖱️ to zoom in on different parts of the plot to see what is happening on **smaller** and **_smaller_** timescales 🔎. You may want to consult the [legend](#🗺️plots-legend) 👇 or [illustrated example](#🧠illustrated-example) 👇.

## ✨Features

Here are some useful features to take note of 🥁: 

1. ✨Plot multiple 🤹, asynchronous (unsampled!) microstructure elements together on the sample plot: <ins>order book quotes</ins>, <ins>trades</ins>, <ins>orders</ins>, <ins>order acks</ins>, <ins>fills<ins> etc.
2. ✨Analyze events on seconds, milliseconds, microseconds, nanoseconds 🕳️ - Zoom in on the most granular time unit available using **Right-click zoom**.
3. ✨All products axes are 🔗linked - zoom in on one product, see what's happening in all others at that same timestamp

## 🧠Illustrated Example

To show why a tool like this might be useful, [here](/examples/README.md) is an example motivated from things seen in the wild.

<ins>Note</ins>: This data was painstakingly created _by hand_ 🤌 to appear quasi-realistic. I am not an artist 🧑‍🎨 nor is this real 🌎 data. 

See the [legend](#🗺️plots-legend) 👇 to understand the plot further.

## 🗺️Plots Legend

[Here](/docs/legend/README.md) is a complete legend of everything the plotter can visualize.

## 💸Free Advice

1. <ins>_Don't log ✏️ in prod_</ins> (unless logging isn't occuring on the hot path). 
2. Make sure the timestamps are from ⏰ <ins>_synchronized clocks_</ins> ⏰ (better if geosync'd/GPS) with enough precision, otherwise these plots will be uninformative or misleading. If you don't trust others' timestamps, do your own capture. 
3. This plotter is _memory intensive_ 🧠. Don't try to plot too much at once. 

## ✏️Data Schema

This plotting module expects a specific data schema that is described [here](/docs/schema/README.md).

## 🤔What is "Market Microstructure"?

_For the uninitiated, here is a ⏰ 30 second primer ⏰ on market microstructure [here](/docs/micro_primer/README.md)_.

## 🛞Installation

You can install the repo using pip directly:

```pip install git+https://github.com/will-thompson-k/microstructure-plotter``` 

Alternatively you can use the setup.py.

## 📜Reqs

Python 3.7+ recommended.

Here are the package requirements (found in requirements.txt)

- [ ] chaco==5.1.0
- [ ] enable==5.3.1
- [ ] traits==6.4.1
- [ ] traitsui==7.4.2
- [ ] pandas==1.3.5
- [ ] pyqt

## 𓊍To Do

- [ ] add more order types: modifies, equity order types, etc.
- [ ] add "decision boundary" of model: bid/ask edges, etc.
- [ ] unit tests

## Citation

```python 
@misc{microstructure-plotter,
  author = {Thompson, Will},
  url = {https://github.com/will-thompson-k/microstructure-plotter},
  year = {2023}
}
```
## License

MIT