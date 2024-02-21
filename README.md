# Bot for vacancies

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Introduction

This is a bot for telegram witch will send you a vacancies in you telegram channel


## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone this repository:
    ```bash
    git clone https://github.com/deyakk7/bot_for_vacancies.git
    ```

2. Navigate to the project directory:
    ```bash
    cd bot_for_vacancies
    ```

3. Build and run the Docker containers using Docker Compose:
    ```bash
    docker-compose up --build
    ```

## Usage

Send to your bot '/start' to start watching a new vacancies. If you want to stop it write '/stop' to bot

## Configuration

### Environment Variables

To run this project, you need to set up the following environment variables in a `.env` file:

- `TOKEN`: Your authentication telegram token for accessing the API.
- `CHANNEL_ID`: The ID of the channel where the bot will operate.
- `DJINNI_URL`: The URL for the Djinni service.
- `WORK_UA_URL`: The URL for the Work.ua service.

Create a `.env` file in the root directory of the project and add the following lines, replacing the placeholders with your actual values:

```plaintext
TOKEN=your_auth_telegram_token
CHANNEL_ID=your_channel_id
DJINNI_URL=https://djinni.co/jobs/
WORK_UA_URL=https://work.ua/jobs/
