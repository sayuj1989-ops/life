# Phase 1, Day 1: Postural Ageing and Control Decline

## Overview
This document summarises key literature found regarding the decline in postural control due to ageing, specifically focusing on proprioception, vestibular degeneration, and cerebellar changes.

## 1. Proprioceptive Decline and Postural Sway
Proprioception is a fundamental component of the human postural control system. With age, the accuracy of proprioceptive signals significantly deteriorates, leading to increased postural sway and compromised dynamic balance.

* **"Age-Related Hip Proprioception Declines: Effects on Postural Sway and Dynamic Balance"**
  * **Authors:** Wingert, Welder, Foo
  * **DOI:** 10.1016/j.apmr.2013.08.012
  * **Key Finding:** Demonstrates a measurable decline in hip proprioceptive accuracy with age, which correlates directly with increases in postural sway and reduced dynamic balance in older adults. This supports the hypothesis of a degrading proprioceptive controller ($K_d$, $K_p$) in our PID model.

* **"A Preliminary Investigation of Hip Proprioception and Postural Sway Parameters of the Young and Elderly."**
  * **Authors:** Bingham, Horsey, Gill
  * **DOI:** 10.1097/01253086-199721050-00044
  * **Key Finding:** Provides preliminary data comparing proprioception and postural sway parameters between young and elderly populations, establishing a baseline difference in postural control capabilities across the lifespan.

## 2. Vestibular Degeneration
The vestibular system, which provides crucial information about head orientation and motion, also undergoes age-related structural and functional decline, compounding the effects of proprioceptive loss.

* **"Vestibular Perception, Balance Impairment, and Fall Risk in Community-Dwelling Older Adults"**
  * **Authors:** Li, Hadi, Smith et al.
  * **DOI:** 10.64898/2026.02.19.26346653
  * **Key Finding:** Links specific impairments in vestibular perception to broader balance issues and a quantitatively higher fall risk among community-dwelling elderly populations.

* **"Can balance function tests predict disability in older adults with peripheral vestibular hypofunction?"**
  * **Authors:** Jasper, Blackington, Gallichio et al.
  * **DOI:** 10.46409/002.crlw5593
  * **Key Finding:** Explores the predictive value of balance function tests for disability in the context of peripheral vestibular hypofunction, highlighting the functional consequences of vestibular degradation.

* **"TRANSGANGLIONIC DEGENERATION IN THE VESTIBULAR NERVE"**
  * **Authors:** GRANT, WESTMAN, EKVALL
  * **DOI:** 10.1016/b978-0-08-015592-0.50037-8
  * **Key Finding:** Provides a physiological mechanism (transganglionic degeneration) for the degradation of vestibular signals, supporting the idea of a physical basis for the increased delay ($\tau$) and reduced gain in the sensory pathways.

## 3. Postural Instability and System-Wide Effects
The culmination of these sensory and neuroanatomical declines results in measurable postural instability, setting the stage for the "terminal derivative gain gap".

* **"The influence of aging and attentional demands on recovery from postural instability"**
  * **Authors:** Stelmach, Zelaznik, Lowe
  * **DOI:** 10.1007/bf03323910
  * **Key Finding:** Shows that ageing not only impairs automatic postural recovery but also increases the attentional demands required to maintain stability, suggesting a shift from lower-level automatic PID control to slower, higher-level cognitive compensation.

* **"Concepts and Methods for Assessing Postural Instability"**
  * **Authors:** Woollacott, Shumway-Cook
  * **DOI:** 10.1123/japa.4.3.214
  * **Key Finding:** Reviews the methodological frameworks for quantifying postural instability, which will be essential for validating the outputs of our geriatric inverted pendulum model.

* **"Commentary: Sensorimotor dysfunction and postural instability in older adults with type 2 diabetes mellitus: the role of proprioception and neuropathy"**
  * **Authors:** Chen, Gong
  * **DOI:** 10.3389/fnagi.2025.1658306
  * **Key Finding:** Highlights how specific conditions (like diabetes) can accelerate proprioceptive decline and neuropathy, serving as an extreme example of the age-related degradation we are modeling.
