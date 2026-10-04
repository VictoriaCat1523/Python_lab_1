import sys

from toolkit.__main__ import main


def run_cli(monkeypatch, capsys, *args):
    """Запускает CLI внутри текущего процесса."""
    monkeypatch.setattr(sys, "argv", ["toolkit", *args])

    try:
        main()
        returncode = 0
    except SystemExit as error:
        returncode = error.code

    captured = capsys.readouterr()

    return returncode, captured.out, captured.err


def test_calc_success(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "calc",
        "2 + 3 * 4",
    )
    assert returncode == 0
    assert stdout.strip() == "14"
    assert stderr == ""

    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "calc",
        "(2 + 3) * 4",
    )
    assert returncode == 0
    assert stdout.strip() == "20"
    assert stderr == ""


def test_calc_error(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "calc",
        "10 / 0",
    )
    assert returncode == 2
    assert stdout == ""
    assert "Деление на ноль" in stderr


def test_convert_success(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "convert",
        "1",
        "--from",
        "km",
        "--to",
        "m",
    )
    assert returncode == 0
    assert stdout.strip() == "1000"
    assert stderr == ""

    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "convert",
        "32",
        "--from",
        "f",
        "--to",
        "c",
    )
    assert returncode == 0
    assert stdout.strip() == "0"
    assert stderr == ""


def test_convert_error(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "convert",
        "1",
        "--from",
        "kg",
        "--to",
        "m",
    )
    assert returncode == 2
    assert stdout == ""
    assert "Несовместимые единицы измерения" in stderr


def test_missing_arguments(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "convert",
        "1",
        "--to",
        "m",
    )
    assert returncode == 2
    assert stdout == ""
    assert "--from" in stderr

    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "convert",
        "1",
        "--from",
        "km",
    )
    assert returncode == 2
    assert stdout == ""
    assert "--to" in stderr


def test_help(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "--help",
    )
    assert returncode == 0
    assert stderr == ""
    assert "calc" in stdout
    assert "convert" in stdout

    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "calc",
        "--help",
    )
    assert returncode == 0
    assert stderr == ""
    assert "expression" in stdout.lower()

    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "convert",
        "--help",
    )
    assert returncode == 0
    assert stderr == ""
    assert "--from" in stdout
    assert "--to" in stdout


def test_invalid_command(monkeypatch, capsys):
    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
        "unknown",
    )
    assert returncode == 2
    assert stdout == ""
    assert stderr != ""

    returncode, stdout, stderr = run_cli(
        monkeypatch,
        capsys,
    )
    assert returncode == 2
    assert stdout == ""
    assert stderr != ""
