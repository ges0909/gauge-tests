# Test Automation with Gauge

## Summary

Jan hatte im Vorfeld des Meetings am 30.04.2020 zur Testautomatisierung vorgeschlagen, auch einmal das
Tool [Gauge](https://gauge.org/) in den Blick zu nehmen. Ich habe daraufhin eine (kurze) Evaluierung vorgenommen.

Vorweg: In Summe sehe ich keine derart ins Auge springenden Vorteile, die eine sofortigen Abkehr vom bisherigen Weg
und den Wechsel zu Gauge rechtfertigen würden.

Im Hinblick auf E2E-Tests mit Browser-Interaktion ist die Kombination Gauge/Taiko trotzdem einen genaueren Blick wert,
auch auf die Gefahr hin, dass wir dann bei den Testwerkzeugen zweigleisig fahren müssten.

Im Einzelnen:

1. Die ursprüngliche Idee, einen bestehenden Test von "MEPS: data cloud" mit Gauge exemplarisch umzusetzen, scheiterte
   an der Unmöglichkeit (nach der erfolgreichen Installation von Gauge selbst), notwendige Plugins (`gauge install python`)
   zu installieren. Es handelt sich aber offensichtlich um ein Problem, dass **nur** im Labor-Netz der VF auftritt.
   Ich werte das deshalb nicht als KO-Kriterium. Siehe dazu auch "_Unresolved installation error on 'Labor-PC'_".

1. Bei der Ausführung des ersten Tests auf einem Rechner ausserhalb des Labor-Netzes trat ein weiterer Fehler auf, den
   ich zum Gegenstand von Github [Issue 1636](https://github.com/getgauge/gauge/issues/1636) gemacht habe. Auch hier
   sehe ich noch kein KO-Kriterium, da das Problem offensichtlich durch einen Versions-Mismatch eines Python-Pakets
   verursacht wurde. Näheres dazu unter "_Workaround 'getgauge' plugin error_".

1. Auf den zweiten Blick sind die Features zur Spezifikation von Tests mit Gauge einerseits und dem YAML-basierten
   Verfahren auf Grundlage von `pytest` andererseits ähnlich. Auffälligster Unterschied ist, dass bei Gauge mit
   seinen Tests als einfache Markdown-Liste Ausführung und Evaluierung in die Implementierung verlagert werden. Beim
   YAML-basierten Verfahren sind Testausführung und -evaluierung voneinader getrennt. Letztere wird im YAML-Skript vom
   Tester und nicht vom Implementierer vorgenommen. Unseres Tests sehen deshalb "technischer" aus, sind aber auch
   flexibler, da der Tester im begrenztem Umfang die Evaluierung selber anpassen kann. Auf der anderen Seite wirkt
   der Markdown-Ansatz von Gauge wegen seiner Einfachheit eleganter und dürfte gerade Nicht-Techniker ansprechen. Man
   muss eben nicht viel wissen, um Tests zu spezifizieren, zu verstehen und auszuführen. Im Übrigen verweise ich auf
   den Abschnitt _"Feature comparison"_ weiter unten.

1. Gauge unterstützt die Ausführung von Tests gegen verschiedene Umgebungen, also das, was wir brauchen. Die Umgebung
   wird auf der Kommandozeile als Option mitgegeben und steht innerhalb der Testimplementierung als "klassische"
   Umgebungsvariablen zur Verfügung. Als Format sind lediglich "old school" Property-Dateien möglich.

1. Test-Reports werden standardmäßig im HTML-Format geschrieben. Allerdings ist optional auch JSON als Ausgabeformat
   möglich, das in einem nachgelagerten Schritt Grundlage für eine PDF-Generierung sein könnte.

1. Die Integration von in der Testimplementierung erzeugter Log-Meldungen in das Gauge-Logging ist möglich, da das in
   _Golang_ implementierte Gauge dafür einen Logger bereitstellt.

1. Gauge Spec's (Testszenarien) können über die Option `--parallel` bei der Ausführung auf mehrere CPU-Kerne verteilt
   werden. Ein sicherlich auch für uns interessantes Feature im Hinblick auf die Möglichkeit, die Ausführung von Tests
   zu beschleunigen. Ich werde das zum Anlass nehmen und prüfen, ob und was `pytest` in dieser Richtung zu bieten hat.
   Davon unberührt bleibt die ohnehin schon vorhandene "Einfach"-Lösung, Tests gleichzeitig in unterschiedlichen
   Konsolenfenstern auszuführen.

1. Gauge bietet die Möglichkeit, wiederkehrende Tests in so genannte _Concept_-Dateien auszulagern, um sie in anderen
   Tests wiederverwenden zu können. Ich finde das ein sehr schönes Feature. Ad-hoc habe ich aber keine Idee, wie wir das
   mit unseren YAML-Skripten nachbilden könnten.

1. Gauge stammt von den Machern von Selenium. Speziell für Web-Tests glaubt man aus den Unzulänglichkeiten von Selenium
   gelernt zu haben und bietet mit [Taiko](https://gauge.org/gauge-taiko/) eine Alternative an, die für Gauge
   Testimplementierung generieren kann. Allerdings nur in _Javascript_, so dass, wenn wir das in Zukunft für E2E-Tests
   würden nutzen wollen, es dann nicht nur mehr mit Python/pytest zu tun haben würden.

## Features comparison

| Feature                    | pytest                | gauge                              |
| :------------------------- | :-------------------- | :--------------------------------- |
| multiple environments      | +                     | +                                  |
| environment data format    | yaml, json            | properties                         |
| test spec. format          | python, yaml          | markdown                           |
| setup/teardown per script  | +                     | +                                  |
| setup/teardown per test    | python + / yaml -     | +                                  |
| test parameterization      | +, includes list      | +, includes table                  |
| file test input            | +                     | +                                  |
| csv file test input        | -                     | +, table                           |
| store values between steps | +                     | +                                  |
| test re-using              | -                     | +, concept files                   |
| tags                       | +, marker             | +                                  |
| skip                       | +                     | -                                  |
| parallel tests             | python ?, yaml -      | +, per CPU kernel                  |
| test report format(s)      | html, pdf             | html, json                         |
| test logging               | +                     | +                                  |
| E2E (web)                  | ?                     | selenium, taiko (js)               |
| IDE                        | PyCharm and others    | VS Code only                       |
| Gauge IDE plugin           | +                     | +                                  |
| IDE debugging              | +                     | +                                  |
| platforms                  | windows, linux, macOS | windows, linux, macOS              |
| test impl. language        | python                | java, js, c#, python, ruby, golang |

## Installing Gauge

### 1. Install Gauge on Windows

- `choco install gauge -y`

```sh
λ gauge --version
Gauge version: 1.0.8
Commit Hash: 28617ea

Plugins
-------
```

Alternative methods as Windows installer or portable Zip file are available.
For details see [Installing Gauge](https://docs.gauge.org/getting_started/installing-gauge.html?os=windows&language=python&ide=vscode).

### 2. Install Gauge plugins

Gauge uses plugins e.g. to bind the language runners which should be used to run the test implementations.

- `gauge install python`

```sh
λ gauge install python
.
Successfully installed plugin 'python' version 0.3.8
```

```sh
λ gauge --version
Gauge version: 1.0.8
Commit Hash: 28617ea

Plugins
-------
python (0.3.8)
```

- `gauge uninstall python`

#### Unresolved installation error on 'Labor-PC'

```sh
C:\Users\Gerrit Schrader\Projekte\sbp-work\GerritS\gauge (master -> origin)
(venv) λ set HTTP_PROXY=http://10.9.4.236:3128

C:\Users\Gerrit Schrader\Projekte\sbp-work\GerritS\gauge (master -> origin)
(venv) λ set HTTPS_PROXY=https://10.9.4.236:3128

C:\Users\Gerrit Schrader\Projekte\sbp-work\GerritS\gauge (master -> origin)
(venv) λ gauge install python
Failed to install plugin 'python'.
Reason: Invalid plugin. Could not download python-install.json file.
...
```

Seems to be a problem caused by the Vodafone environment.

## Creating a test project

- available templates: `gauge init --templates`
- `mkdir gauge-tests && cd gauge-tests`
- `gauge init python`

```sh
λ gauge init python
Downloading python.zip
.
Copying Gauge template python to current directory ...
Successfully initialized the project. Run specifications with "gauge run specs/".
```

```sh
λ ls -lrt
total 2
-rw-r--r-- 1 Gerrit 197609  9 Mai  1 09:51 requirements.txt
-rw-r--r-- 1 Gerrit 197609 64 Mai  1 09:51 manifest.json
drwxr-xr-x 1 Gerrit 197609  0 Mai  1 09:51 env/
drwxr-xr-x 1 Gerrit 197609  0 Mai  1 09:51 specs/
drwxr-xr-x 1 Gerrit 197609  0 Mai  1 09:51 step_impl/
```

### Workaround 'getgauge' plugin error

When running tests with `gauge runs specs/` a bunch of errors appear on console. I have reported this to the _getgauge_
plugin owners with [Issue 1636](https://github.com/getgauge/gauge/issues/1636).

As workaround the plugin was installed as python package from [The Python Package Index](https://pypi.org/project/getgauge/). This also results in errors but tests seems to be executed.

- `pip install getgauge`

## Running a specification

- `gauge run specs/`

```sh
Python: 3.8.2
# Specification Heading
  ## Vowel counts in single word         P P
  ## Vowel counts in multiple word       P P

Successfully generated html-report to => C:\Users\Gerrit\Desktop\gauge-tests\reports\html-report\index.html

Specifications: 1 executed      1 passed        0 failed        0 skipped
Scenarios:      2 executed      2 passed        0 failed        0 skipped

Total time taken: 118ms
```

Other examples:

- `gauge run --parallel specs/`
- `gauge run --parallel -n 2 specs/` # '-n' = number of CPU cores
- `gauge run --tags successful specs/`
- `gauge run --tags "successful & other" specs/`
- `gauge --env dev --log-level INFO run specs/`
- `gauge --env dev --log-level INFO --machine-readable run specs/`

## IDE support

- only [VS Code](https://code.visualstudio.com/) with [Gauge](https://marketplace.visualstudio.com/items?itemName=getgauge.gauge) extension
- debugging test implementations is possible in VS Code and works fine
- further VS Code extension required to support test implementations in python, e.g.
  - [black](https://black.readthedocs.io/en/stable/) formatter
  - [mypy](http://mypy-lang.org/) optional static type checker
- for IntelliJ products only for IDEA (Java), but **not** for PyCharm (Python)

## Write Spec's

- Tests are written in [Markdown](https://daringfireball.net/projects/markdown/basics) syntax and stored in specification files, briefly referred to as _Spec_.
- A spec contains a single or multiple scenarios.
- Lists within scenarios specify test steps.
- Tags

## Implement steps

- `@before*` and `@after*` hooks
- use of Python's `assert` to evaluate test results

## Reports

- generates HTML reports
- `gauge install json-report`

## E2E

- browser-based tests with `Taiko`
- _node_ package, requires JS
- see: [Testing with Gauge](https://blog.ippon.tech/testing-with-gauge/)

## Appendix

### Spec

```markdown
# RESTful API Tests

## Get resources

- make a 'delete' request
- make a 'get' request
- make a 'patch' request
- make a 'post' request
- make a 'put' request

## Request modem profiles

- if profile with with type X is requested, then profile X is returned

  | type    | profile            |
  | ------- | ------------------ |
  | ping    | pingProfileType    |
  | general | generalProfileType |
```

### Implementation

```python
import http
import json
import os
import pprint

import requests
from getgauge import logger
from getgauge.python import (
    DataStore,
    DataStoreFactory,
    after_scenario,
    after_spec,
    after_step,
    before_scenario,
    before_spec,
    before_step,
    step,
)


@before_spec()
def before_spec_hook(context):
    logger.debug(f">> before_spec_hook: {context}")


@before_scenario()
def before_scenario_hook(context):
    logger.debug(f">> before_scenario_hook: {context}")


@before_step()
def before_step_hook(context):
    logger.debug(f">> before_step_hook: {context}")


@after_spec()
def after_spec_hook(context):
    logger.debug(f">> after_spec_hook: {context}")


@after_scenario()
def after_scenario_hook(context):
    logger.debug("f>> after_scenario_hook: {context}")


@after_step()
def after_step_hook(context):
    logger.debug(f">> after_step_hook: {context}")


def http_logging(resp, *args, **kwargs):
    logger.debug(f"<< {resp.status_code} {pprint.pformat(resp.json())}")


@step("make a 'delete' request")
def delete():
    store = DataStoreFactory.scenario_data_store()
    store.put("op", "delete")
    endpoint = os.getenv("endpoint") + "/delete"
    response = requests.delete(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("make a 'get' request")
def get():
    endpoint = os.getenv("endpoint") + "/get"
    response = requests.get(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint
    store = DataStoreFactory.scenario_data_store()
    assert store.get("op") == "delete"


@step("make a 'patch' request")
def patch():
    endpoint = os.getenv("endpoint") + "/patch"
    response = requests.patch(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("make a 'post' request")
def post():
    endpoint = os.getenv("endpoint") + "/post"
    response = requests.post(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("make a 'put' request")
def put():
    endpoint = os.getenv("endpoint") + "/put"
    response = requests.put(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("if profile with with type X is requested, then profile X is returned <table>")
def get_profile(table):
    for type, name in table.rows:
        pass
```

### Running Spec

```sh
λ gauge run specs\rest.spec
Der Befehl ""C:\Python38\python.exe -m pip install getgauge==0.3.8 --user"" ist entweder falsch geschrieben oder konnte nicht gefunden werden.
Traceback (most recent call last):
File "check_and_install_getgauge.py", line 40, in <module>
assert_versions()
File "check_and_install_getgauge.py", line 34, in assert_versions
install_getgauge("getgauge=="+expected_gauge_version)
File "check_and_install_getgauge.py", line 20, in install_getgauge
check_output([" ".join(install_cmd)], shell=True)
File "C:\Python38\lib\subprocess.py", line 411, in check_output
return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
File "C:\Python38\lib\subprocess.py", line 512, in run
raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['C:\\Python38\\python.exe -m pip install getgauge==0.3.8 --user']' returned non-zero exit status 1.
Python: 3.8.2
# RESTful API Tests
  ## Get resources       PC:\Users\Gerrit\Desktop\gauge-tests\step_impl\rest_impl.py:71: DeprecationWarning: 'DataStoreFactory.scenario_data_store()' is deprecated in favour of 'data_store.scenario'
store = DataStoreFactory.scenario_data_store()
 P P P P
  ## Request modem profiles      P

Successfully generated json-report to => C:\Users\Gerrit\Desktop\gauge-tests\reports\json-report

Successfully generated html-report to => C:\Users\Gerrit\Desktop\gauge-tests\reports\html-report\index.html

Specifications: 1 executed      1 passed        0 failed        0 skipped
Scenarios:      2 executed      2 passed        0 failed        0 skipped

Total time taken: 3.213s
```
